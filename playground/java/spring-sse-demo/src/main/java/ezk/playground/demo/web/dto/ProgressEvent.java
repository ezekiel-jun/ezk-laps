package ezk.playground.demo.web.dto;

import java.time.Instant;

public record ProgressEvent(
        String step,         // "a" | "b" | "c" | "end" | "error"
        String status,       // "START" | "IN_PROGRESS" | "DONE" | "ERROR"
        String message,      // 설명
        Integer percent,     // 0~100 (null 가능)
        Instant timestamp
) {
    public static ProgressEvent of(String step, String status, String msg, Integer pct) {
        return new ProgressEvent(step, status, msg, pct, Instant.now());
    }
}