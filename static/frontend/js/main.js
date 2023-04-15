const domBanner = document.querySelectorAll('[data-lazyload-image]');

let callbackObserverBanner = (entries, observer) => {
  entries.forEach((e) => {
    if (e.isIntersecting) {
      if (e.target.dataset.lazyloadImage !== undefined) {
        e.target.removeAttribute('data-lazyload-image');
        e.target.src = e.target.dataset.imgSrc;
        imagesLoaded(e.target, function (instance) {
          if (e.target.complete) {
            setTimeout(() => {
              e.target.classList.remove('image__blur');
            });
          } else {
            e.target.addEventListener('load', function () {
              setTimeout(() => {
                e.target.classList.remove('image__blur');
              }, 1);
            });
          }
        });
        e.target.removeAttribute('data-lazyload-image');
      }
    }
  });
};

let observer = new IntersectionObserver(callbackObserverBanner, {
  root: null,
  rootMargin: '0px',
  threshold: 0.95,
});
domBanner.forEach((domImage) => {
  observer.observe(domImage);
});
