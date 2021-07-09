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