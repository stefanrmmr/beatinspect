const timeMilliSec = 5000

navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();
    const audioChunks = [];
    mediaRecorder.addEventListener("dataavailable", event => {
      audioChunks.push(event.data);
    });
    mediaRecorder.addEventListener("stop", () => {
      //convert audioBuffer to wav
      const audioBlob = new Blob(audioChunks, {type:'audio/wav'});
      //create base64 reader
      var reader = new FileReader();
      reader.readAsDataURL(audioBlob);
      reader.onloadend = function() {
        //read base64
        var base64data = reader.result;
        //send data to streamlit
        document.dispatchEvent(new CustomEvent("GET_AUDIO_BASE64", {detail: base64data}));
      }
    });
    setTimeout(() => {
      mediaRecorder.stop();
    }, timeMilliSec);
  });
