package ezk.playground.demo.web.dto;

@FunctionalInterface
public interface ProgressReporter {
    void report(ProgressEvent event);

    default boolean isCancelled() { return false; }
    default void onCancelled() {}
}