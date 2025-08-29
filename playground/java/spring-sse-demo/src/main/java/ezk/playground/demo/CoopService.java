package ezk.playground.demo;

import ezk.playground.demo.web.dto.ProgressEvent;
import ezk.playground.demo.web.dto.ProgressReporter;
import ezk.playground.demo.web.dto.RequestDto;
import ezk.playground.demo.web.dto.ResponseDto;
import org.springframework.stereotype.Service;

@Service
public class CoopService {

    public ResponseDto run(RequestDto req, ProgressReporter reporter) throws Exception {
        // Step A
        reporter.report(ProgressEvent.of("a", "START", "A 작업 시작", 0));
        simulateBlockingWork(400);
        reporter.report(ProgressEvent.of("a", "IN_PROGRESS", "A 40%", 40));
        simulateBlockingWork(400);
        reporter.report(ProgressEvent.of("a", "DONE", "A 완료", 100));

        // Step B
        reporter.report(ProgressEvent.of("b", "START", "B 작업 시작", 0));
        simulateBlockingWork(300);
        reporter.report(ProgressEvent.of("b", "IN_PROGRESS", "B 50%", 50));
        simulateBlockingWork(300);
        reporter.report(ProgressEvent.of("b", "DONE", "B 완료", 100));

        // Step C
        reporter.report(ProgressEvent.of("c", "START", "C 작업 시작", 0));
        simulateBlockingWork(500);
        reporter.report(ProgressEvent.of("c", "IN_PROGRESS", "C 75%", 75));
        simulateBlockingWork(500);
        reporter.report(ProgressEvent.of("c", "DONE", "C 완료", 100));

        // 최종 결과(기존 전통식 반환)
        return new ResponseDto(req.jobId(), "ALL DONE", true);
    }

    private void simulateBlockingWork(long millis) throws InterruptedException {
        Thread.sleep(millis);
    }
}