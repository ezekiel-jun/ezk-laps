package ezk.playground.demo;

import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;

import java.time.Duration;

@Service
public class WorkService {

    public Flux<String> a() {
        return Flux.concat(
                Flux.just("A: START").delayElements(Duration.ofMillis(500)),
                Flux.just("A: IN_PROGRESS 30%").delayElements(Duration.ofMillis(500)),
                Flux.just("A: IN_PROGRESS 60%").delayElements(Duration.ofMillis(500)),
                Flux.just("A: DONE").delayElements(Duration.ofMillis(500))
        );
    }

    public Flux<String> b() {
        return Flux.concat(
                Flux.just("B: START").delayElements(Duration.ofMillis(500)),
                Flux.just("B: IN_PROGRESS 50%").delayElements(Duration.ofMillis(500)),
                Flux.just("B: DONE").delayElements(Duration.ofMillis(500))
        );
    }

    public Flux<String> c() {
        return Flux.concat(
                Flux.just("C: START").delayElements(Duration.ofMillis(500)),
                Flux.just("C: IN_PROGRESS 25%").delayElements(Duration.ofMillis(500)),
                Flux.just("C: IN_PROGRESS 75%").delayElements(Duration.ofMillis(500)),
                Flux.just("C: DONE").delayElements(Duration.ofMillis(500))
        );
    }
}
