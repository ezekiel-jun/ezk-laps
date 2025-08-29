package ezk.playground.demo.web;

import ezk.playground.demo.CoopService;
import ezk.playground.demo.web.dto.*;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.FluxSink;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

import java.time.Instant;
import java.util.concurrent.atomic.AtomicBoolean;

@RestController
@RequestMapping("/api/coop")
public class CoopSseController {

    private final CoopService coopService;

    public CoopSseController(CoopService coopService) {
        this.coopService = coopService;
    }

    @PostMapping(
            value = "/run",
            consumes = MediaType.APPLICATION_JSON_VALUE,
            produces = MediaType.TEXT_EVENT_STREAM_VALUE
    )
    public Flux<ServerSentEvent<EventEnvelope>> run(@RequestBody RequestDto req) {
        return Flux.create((FluxSink<ServerSentEvent<EventEnvelope>> sink) -> {
            AtomicBoolean cancelled = new AtomicBoolean(false);

            ProgressReporter reporter = ev -> {
                if (!cancelled.get()) {
                    sink.next(sse("progress", "progress", ev));
                }
            };

            Mono.fromCallable(() -> coopService.run(req, reporter))
                    .subscribeOn(Schedulers.boundedElastic())
                    .doOnSuccess((ResponseDto res) -> {
                        sink.next(sse("result", "result", res)); // 최종 결과 DTO 1회
                        sink.next(sse("progress", "progress",
                                      ProgressEvent.of("end", "DONE", "모든 작업 종료", 100)));
                        sink.complete();
                    })
                    .doOnError(ex -> {
                        sink.next(sse("error", "error",
                                      ProgressEvent.of("error", "ERROR", "오류: " + ex.getMessage(), null)));
                        sink.complete();
                    })
                    .subscribe();

            sink.onCancel(() -> cancelled.set(true));
            sink.onDispose(() -> cancelled.set(true));
        }, FluxSink.OverflowStrategy.BUFFER);
    }

    private ServerSentEvent<EventEnvelope> sse(String event, String kind, Object payload) {
        return ServerSentEvent.<EventEnvelope>builder()
                .id(String.valueOf(System.nanoTime()))
                .event(event) // "progress" | "result" | "error"
                .data(new EventEnvelope(kind, payload, Instant.now()))
                .build();
    }
}