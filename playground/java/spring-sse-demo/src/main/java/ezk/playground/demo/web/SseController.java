package ezk.playground.demo.web;
import ezk.playground.demo.SsePayload;
import ezk.playground.demo.WorkService;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

import java.time.Instant;

@RestController
public class SseController {

    private final WorkService work;

    public SseController(WorkService work) {
        this.work = work;
    }

    /**
     * (1) GET /api/sse/run
     * - 요청 1번으로 a→b→c 순차 실행
     * - 각 단계 완료 시 SSE 이벤트 전송
     * - 마지막에 end 이벤트 전송
     */
    @GetMapping(value = "/api/sse/run", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<SsePayload>> run() {

        var start = event("a", "START", "Step A 시작");
        var a = work.a().map(res -> event("a", "DONE", "Step A 완료: " + res));

        var bstart = event("b", "START", "Step B 시작");
        var b = work.b().map(res -> event("b", "DONE", "Step B 완료: " + res));

        var cstart = event("c", "START", "Step C 시작");
        var c = work.c().map(res -> event("c", "DONE", "Step C 완료: " + res));

        var end = event("end", "DONE", "모든 작업 종료");

        // 순차로 흘러가도록 concat 사용
        return Flux.concat(
                        Flux.just(start),
                        a,
                        Flux.just(bstart),
                        b,
                        Flux.just(cstart),
                        c,
                        Flux.just(end)
                )
                // (선택) keep-alive 용 ping 이벤트를 합치고 싶다면 아래처럼 interval Flux를 merge할 수 있음.
                // .mergeWith(Flux.interval(Duration.ofSeconds(15)).map(i -> ping()))
                .onErrorResume(ex ->
                                       Flux.just(error("error", "ERROR", "오류: " + ex.getMessage()))
                );
    }

    private ServerSentEvent<SsePayload> event(String step, String status, String msg) {
        return ServerSentEvent.<SsePayload>builder()
                .id(String.valueOf(System.nanoTime()))
                .event("message")
                .data(new SsePayload(step, status, msg, Instant.now()))
                .build();
    }

    private ServerSentEvent<SsePayload> error(String step, String status, String msg) {
        return ServerSentEvent.<SsePayload>builder()
                .id(String.valueOf(System.nanoTime()))
                .event("error")
                .data(new SsePayload(step, status, msg, Instant.now()))
                .build();
    }

    // 필요 시 ping 이벤트
    // private ServerSentEvent<SsePayload> ping() {
    //   return ServerSentEvent.<SsePayload>builder()
    //       .event("ping")
    //       .data(new SsePayload("ping", "IN_PROGRESS", "keep-alive", Instant.now()))
    //       .build();
    // }
}
