/* summernote-file-upload.js
   Summernote plugin: add a 'fileupload' button that allows inserting a file
   reference. This is a lightweight client-side helper that inserts the
   filename as a text/link. Real server upload integration can replace the
   `handleFile` implementation.
*/
(function(window, $){
  'use strict';
  if (typeof $ === 'undefined' || !$.summernote) {
    // Defer registration if Summernote isn't available yet
    window._inqedSummernoteFileUpload = window._inqedSummernoteFileUpload || [];
    window._inqedSummernoteFileUpload.push(function(){
      registerPlugin($);
    });
    return;
  }

  function registerPlugin($){
    if (!$.summernote) return;
    if ($.summernote.plugins && $.summernote.plugins._inqed_fileupload_registered) return;

    // Add a button to the toolbar named 'fileupload'
    $.summernote.addButton('fileupload', function(context){
      var ui = $.summernote.ui;
      var button = ui.button({
        contents: '<i class="far fa-file"></i>',
        tooltip: 'Insert file',
        click: function(){
          // create a hidden file input and trigger it
          var input = document.createElement('input');
          input.type = 'file';
          input.style.display = 'none';
          input.addEventListener('change', function(ev){
            var file = input.files && input.files[0];
            if (!file) return;
            handleFile(file, context);
            // cleanup
            setTimeout(function(){ input.remove(); }, 1000);
          });
          document.body.appendChild(input);
          input.click();
        }
      });
      return button.render();
    });

    // expose a no-op upload handler (replace with real upload if needed)
    function handleFile(file, context){
      try{
        var form = new FormData();
        form.append('file', file);
        fetch('{% url "summernote_upload" %}', {
          method: 'POST',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': (document.cookie||'').split('csrftoken=')[1] || ''
          },
          body: form
        }).then(function(r){ return r.json(); }).then(function(js){
          if (js && js.success && js.url){
            // insert an <a> for generic files or <img> for images
            if (file.type.indexOf('image/') === 0) {
              context.invoke('editor.insertImage', js.url);
            } else {
              var a = document.createElement('a');
              a.href = js.url;
              a.textContent = file.name;
              context.invoke('editor.insertNode', a);
            }
          } else {
            console.warn('upload failed', js);
          }
        }).catch(function(err){ console.error('upload error', err); });
      }catch(e){
        console.error('file upload handler failed', e);
      }
    }

    // mark registered
    $.summernote.plugins._inqed_fileupload_registered = true;
    console.debug('Registered summernote fileupload button');
  }

  // Register immediately if jQuery + Summernote are present
  if ($ && $.summernote) registerPlugin($);

  // If registration was deferred earlier, attempt to run queued registrations
  if (window._inqedSummernoteFileUpload && Array.isArray(window._inqedSummernoteFileUpload)){
    var q = window._inqedSummernoteFileUpload.slice();
    window._inqedSummernoteFileUpload = [];
    q.forEach(function(fn){ try{ fn(); }catch(e){} });
  }

})(window, window.jQuery);
