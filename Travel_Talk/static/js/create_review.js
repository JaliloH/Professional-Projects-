// SOURCES: https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsDataURL
//         https://stackoverflow.com/questions/72550576/save-image-files-as-bytea-in-postgresql-and-retrieving-them-to-display-on-html-t

// function previewFile() {
//     const preview = document.getElementById('upload-image');
//     const file = document.querySelector('input[type=file]').files[0];
//     const reader = new FileReader();
  
//     reader.addEventListener("load", function () {
//       // convert image file to base64 string
//       preview.src = reader.result;
//       b64.innerHTML = reader.result; // show in textarea
//     }, false);
  
//     if (file) {
//       reader.readAsDataURL(file);
//     }
// }

function previewFiles() {
    const preview = document.querySelector("#preview");
    const files = document.querySelector("input[type=file]").files;
  
    function readAndPreview(file) {
      // Make sure `file.name` matches our extensions criteria
      if (/\.(jpe?g|png|gif)$/i.test(file.name)) {
        const reader = new FileReader();
  
        reader.addEventListener(
          "load",
          () => {
            const image = new Image();
            image.height = 100;
            image.title = file.name;
            image.src = reader.result;
            preview.appendChild(image);
          },
          false,
        );
  
        reader.readAsDataURL(file);
      }
    }
  
    if (files) {
      Array.prototype.forEach.call(files, readAndPreview);
    }
  }
  
  const picker = document.querySelector("#create-image-button");
  picker.addEventListener("change", previewFiles);