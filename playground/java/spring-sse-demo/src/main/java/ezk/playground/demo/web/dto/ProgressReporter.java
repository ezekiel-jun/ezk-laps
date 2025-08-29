package ezk.playground.demo.web.dto;

@FunctionalInterface
public interface ProgressReporter {
    void report(ProgressEvent event);

    // (선택) 취소 신호가 필요한 경우 확장
    default boolean isCancelled() { return false; }
    default void onCancelled() {}
}
