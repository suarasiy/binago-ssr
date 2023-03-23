const initMenu = () => {
  const getMenus = document.querySelectorAll('[data-target-menu]');
  getMenus.forEach((e) => {
    if (e.querySelector('.indicator').classList.contains('indicator--active')) {
      document.querySelector(`#${e.getAttribute('data-target-menu')}`).style.maxHeight =
        document.querySelector(`#${e.getAttribute('data-target-menu')}`).scrollHeight + 'px';
      document.querySelector(`#${e.getAttribute('data-target-menu')}`).classList.remove('nav__sub__menu--hide');
    } else {
      document.querySelector(`#${e.getAttribute('data-target-menu')}`).style.maxHeight = '0px';
      document.querySelector(`#${e.getAttribute('data-target-menu')}`).classList.add('nav__sub__menu--hide');
    }
    e.addEventListener('click', () => {
      const target = document.querySelector(`#${e.getAttribute('data-target-menu')}`);
      const state = e.querySelector('.indicator');
      target.style.maxHeight = '0px';
      if (state.classList.contains('indicator--active')) {
        target.style.maxHeight = '0px';
        state.classList.remove('indicator--active');
        document.querySelector(`#${e.getAttribute('data-target-menu')}`).classList.add('nav__sub__menu--hide');
        return;
      }
      target.style.maxHeight = target.scrollHeight + 'px';
      state.classList.add('indicator--active');
      document.querySelector(`#${e.getAttribute('data-target-menu')}`).classList.remove('nav__sub__menu--hide');
    });
  });
};

initMenu();
