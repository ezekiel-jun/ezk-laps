package ezk.playground.demo.web.dto;

import java.time.Instant;

public record EventEnvelope(
        String kind,     // "progress" | "result" | "error" 등
        Object payload,  // ProgressEvent or ResponseDto 등 실제 데이터
        Instant at       // 타임스탬프
) {}
