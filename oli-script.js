function togglePicture() {
    if (document.getElementById("oliviero-picture").style.display == 'inline') {
        document.getElementById("oliviero-picture").style.display = 'none';
        document.getElementById("picture-credits-text").style.display = 'none';
        
    }
    else {
        document.getElementById("oliviero-picture").style.display = 'inline';
        document.getElementById("picture-credits-text").style.display = 'inline';
    }
}