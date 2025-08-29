package ezk.playground.demo;

import java.time.Instant;

public record SsePayload(
        String step,         // "a" | "b" | "c" | "end" | "error"
        String status,       // "START" | "IN_PROGRESS" | "DONE" | "ERROR"
        String message,      // 설명 메시지
        Instant timestamp    // 이벤트 발생 시각
) {}