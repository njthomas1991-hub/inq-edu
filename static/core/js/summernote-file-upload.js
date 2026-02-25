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
        var reader = new FileReader();
        reader.onload = function(){
          // Insert a simple link with the filename. For real uploads,
          // upload to server and insert returned URL instead.
          var txt = document.createElement('a');
          txt.href = '#';
          txt.textContent = file.name;
          context.invoke('editor.insertNode', txt);
        };
        // read as data just to trigger the onload; not used here
        reader.readAsArrayBuffer(file.slice(0,1));
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
