package ezk.playground.demo.web.dto;

import ezk.playground.demo.web.type.NodeProgressStatus;
import ezk.playground.demo.web.type.Result;
import ezk.playground.demo.web.type.WorkflowProgressStatus;

import java.time.Instant;

public record ProgressEvent(
        String step,         // "a" | "b" | "c" | "end" | "error"
        WorkflowProgressStatus workflowProgressStatus,
        NodeProgressStatus nodeProgressStatus,
        Result result,
        String errorCode,
        String message,      // 설명
        Integer percent,     // 0~100 (null 가능)
        Instant timestamp
) {
    public static ProgressEvent of (String step,
                                    WorkflowProgressStatus workflowProgressStatus,
                                    NodeProgressStatus nodeProgressStatus,
                                    Result result,
                                    String errorCode,
                                    String message,
                                    Integer pct) {
        return new ProgressEvent(step, workflowProgressStatus, nodeProgressStatus, result, errorCode, message, pct, Instant.now());
    }
}