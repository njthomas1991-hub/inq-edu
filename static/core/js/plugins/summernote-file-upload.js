// Custom Summernote plugin for file/document upload
(function(factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as anonymous module.
    define(['jquery'], factory);
  } else if (typeof module === 'object' && module.exports) {
    // Node/CommonJS
    module.exports = factory(require('jquery'));
  } else {
    // Browser globals
    factory(window.jQuery);
  }
}(function($) {
  $.extend($.summernote.plugins, {
    'fileupload': function(context) {
      var self = this;
      var ui = $.summernote.ui;
      var $editor = context.layoutInfo.editor;
      var $editable = context.layoutInfo.editable;
      var options = context.options;
      var lang = options.langInfo;

      // Add button to toolbar
      context.memo('button.fileupload', function() {
        return ui.button({
          contents: '<i class="fas fa-paperclip"></i>',
          tooltip: 'Insert File',
          click: function() {
            self.showFileDialog();
          }
        }).render();
      });

      // Show file dialog
      this.showFileDialog = function() {
        var $fileInput = $('<input type="file" style="display:none;" />');
        $fileInput.appendTo('body');
        $fileInput.trigger('click');
        $fileInput.on('change', function() {
          var file = this.files[0];
          if (file) {
            self.uploadFile(file);
          }
          $fileInput.remove();
        });
      };

      // Upload file to server
      this.uploadFile = function(file) {
        var formData = new FormData();
        formData.append('file', file);
        // CSRF token for Django
        var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
          url: '/summernote/file-upload/',
          type: 'POST',
          data: formData,
          processData: false,
          contentType: false,
          headers: {'X-CSRFToken': csrftoken},
          success: function(data) {
            if (data.url) {
              var link = '<a href="' + data.url + '" target="_blank">' + file.name + '</a>';
              context.invoke('editor.pasteHTML', link);
            } else {
              alert('File upload failed.');
            }
          },
          error: function() {
            alert('File upload failed.');
          }
        });
      };
    }
  });
}));
