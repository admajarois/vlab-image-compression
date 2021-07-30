function showImageBellow(imgs) {
    const expandImg = document.getElementById("expandedImg");
    expandImg.src = imgs.src;
    expandImg.parentElement.style.display = "block";

}

const preview = ()=>{
    const image = document.querySelector('#image')
    const label = document.querySelector('.custom-file-label')
    const imgPreview = document.querySelector('.img-preview')

    label.textContent = image.files[0].name;
    console.log(image);

    const fileImg = new FileReader();
    fileImg.readAsDataURL(image.files[0]);

    fileImg.onload=(e)=>{
        imgPreview.src = e.target.result;
    }
}

function previewImageOriginal() {
    document.getElementById("image-preview-original").style.display = "block";
    var oFReader = new FileReader();
     oFReader.readAsDataURL(document.getElementById("original-image").files[0]);
 
    oFReader.onload = function(oFREvent) {
      document.getElementById("image-preview-original").src = oFREvent.target.result;
    };
};

function previewImageCompress() {
    document.getElementById("image-preview-compressed").style.display = "block";
    var oFReader = new FileReader();
     oFReader.readAsDataURL(document.getElementById("compressed-image").files[0]);
 
    oFReader.onload = function(oFREvent) {
      document.getElementById("image-preview-compressed").src = oFREvent.target.result;
    };
};

