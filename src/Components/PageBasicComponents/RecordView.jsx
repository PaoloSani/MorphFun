import { useRef } from "react";
import { useReactMediaRecorder } from "react-media-recorder";


const RecordView = ({}) => {
  const { startRecording, stopRecording, mediaBlobUrl } = useReactMediaRecorder(
    { video: true }
  );

  const $audio = useRef(null);



  return (
    <div>
      <button id={"record"} onClick={startRecording}>
        Start Recording
      </button>
      <button
        id={"stop"}
        onClick={() => {
          stopRecording();
        }}
      >
        Stop Recording
      </button>
      <audio ref={$audio} id={"player"} src={mediaBlobUrl} controls />
    </div>
  );
};

export default RecordView;
