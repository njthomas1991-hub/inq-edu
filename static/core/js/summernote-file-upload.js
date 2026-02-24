// Minimal Summernote file upload plugin shim (placeholder)
(function(){
  if (typeof window.jQuery === 'undefined') return;
  // register a dummy button if Summernote exists later
  try {
    (window._inqedSummernoteFileUpload = true);
    console.debug('summernote-file-upload.js placeholder loaded');
  } catch(e){}
})();
