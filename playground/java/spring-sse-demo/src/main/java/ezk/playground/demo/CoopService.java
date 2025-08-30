package ezk.playground.demo;

import ezk.playground.demo.web.dto.ProgressEvent;
import ezk.playground.demo.web.dto.ProgressReporter;
import ezk.playground.demo.web.dto.RequestDto;
import ezk.playground.demo.web.dto.ResponseDto;
import ezk.playground.demo.web.type.NodeProgressStatus;
import ezk.playground.demo.web.type.Result;
import ezk.playground.demo.web.type.WorkflowProgressStatus;
import org.springframework.stereotype.Service;

@Service
public class CoopService {

    public ResponseDto run(RequestDto req, ProgressReporter reporter) throws Exception {
        // A 단계
        reporter.report(ProgressEvent.of(
                "a", WorkflowProgressStatus.STARTED, NodeProgressStatus.EXECUTING,
                null, null, "A 작업 시작", 0));
        simulate(400);
        reporter.report(ProgressEvent.of(
                "a", WorkflowProgressStatus.RUNNING, NodeProgressStatus.EXECUTING,
                null, null, "A 40%", 40));
        simulate(400);
        reporter.report(ProgressEvent.of(
                "a", WorkflowProgressStatus.RUNNING, NodeProgressStatus.FINISHED,
                Result.SUCCESS, null, "A 완료", 100));

        // B 단계
        reporter.report(ProgressEvent.of(
                "b", WorkflowProgressStatus.RUNNING, NodeProgressStatus.EXECUTING,
                null, null, "B 작업 시작", 0));
        simulate(300);
        reporter.report(ProgressEvent.of(
                "b", WorkflowProgressStatus.RUNNING, NodeProgressStatus.EXECUTING,
                null, null, "B 50%", 50));
        simulate(300);
        reporter.report(ProgressEvent.of(
                "b", WorkflowProgressStatus.RUNNING, NodeProgressStatus.FINISHED,
                Result.SUCCESS, null, "B 완료", 100));

        // C 단계
        reporter.report(ProgressEvent.of(
                "c", WorkflowProgressStatus.RUNNING, NodeProgressStatus.EXECUTING,
                null, null, "C 작업 시작", 0));
        simulate(500);
        reporter.report(ProgressEvent.of(
                "c", WorkflowProgressStatus.RUNNING, NodeProgressStatus.EXECUTING,
                null, null, "C 75%", 75));
        simulate(500);
        reporter.report(ProgressEvent.of(
                "c", WorkflowProgressStatus.RUNNING, NodeProgressStatus.FINISHED,
                Result.SUCCESS, null, "C 완료", 100));

        // 전통식 최종 반환
        return new ResponseDto(req.jobId(), "ALL DONE", true);
    }

    private void simulate(long millis) throws InterruptedException {
        Thread.sleep(millis);
    }

}