function openImage(idmodal) {
  const elementModal = '#' + idmodal + '.space_modal';
  const overlay = document.getElementById('overlayImage');
  const enlargedImage = document.getElementById('enlargedImage');
  const modalDiv = document.querySelector(elementModal);
  // enlargedImage.src = src;
  enlargedImage.innerHTML = modalDiv.outerHTML;
  enlargedImage.querySelector(elementModal).style.display = 'flex';
  overlay.style.display = 'flex';
}

function closeImage() {
  const overlay = document.getElementById('overlayImage');
  overlay.style.display = 'none';
}


document.querySelectorAll('.clickable-image').forEach(button => {
  button.addEventListener('click', function (event) {
    // openImage(event.target.id);
    openImage(button.id);
  });
});


// document.addEventListener('click', function(event) {
//   if (event.target.classList.contains('clickable-image')) {
//     openImage(event.target.id);
//   }
// });







// function openImage(src) {
//   const overlay = document.getElementById('overlayImage');
//   const enlargedImage = document.getElementById('enlargedImage');

//   enlargedImage.src = src;
//   overlay.style.display = 'flex';
// }

// function closeImage() {
//   const overlay = document.getElementById('overlayImage');
//   overlay.style.display = 'none';
// }

// document.addEventListener('click', function(event) {
//   if (event.target.classList.contains('clickable-image')) {
//     openImage(event.target.src);
//   }
// });

