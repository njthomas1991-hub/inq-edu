/* core/js/main.js
   General small UI helpers used across the site. Keeps behaviour unobtrusive
   and defensive so missing features don't break pages.
*/
(function(){
  'use strict';

  function onReady(fn){
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  function initNavbarDropdowns(){
    // Ensure bootstrap dropdowns work when anchors use '#'
    document.querySelectorAll('.navbar .dropdown-toggle').forEach(function(btn){
      btn.addEventListener('click', function(e){
        // allow bootstrap to handle toggle, but prevent accidental navigation
        if (btn.getAttribute('href') === '#') e.preventDefault();
      });
    });
  }

  function initSkipLink(){
    var skip = document.querySelector('.skip-to-main');
    if (!skip) return;
    skip.addEventListener('click', function(e){
      var target = document.getElementById('main-content');
      if (target){
        target.setAttribute('tabindex','-1');
        target.focus({preventScroll:true});
      }
    });
  }

  onReady(function(){
    try{
      initNavbarDropdowns();
      initSkipLink();
      console.debug('core/js/main.js initialized');
    }catch(e){
      console.error('main.js init error', e);
    }
  });

  // expose a small helper for other scripts
  window.INQED = window.INQED || {};
  window.INQED.helpers = {
    focusMain: function(){
      var t = document.getElementById('main-content'); if (t){ t.setAttribute('tabindex','-1'); t.focus(); }
    }
  };
})();
