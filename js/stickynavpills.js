/**
 * jQuery Plugin: Sticky Tabs
 *
 * @author Aidan Lister <aidan@php.net>
 * @version 1.0.0
 */
(function ( $ ) {
    $.fn.stickyTabs = function() {
        context = this
        // Show the tab corresponding with the hash in the URL, or the first tab.
        var showTabFromHash = function() {
          var hash = window.location.hash;
          var selector = hash ? 'a[href="' + hash + '"]' : 'li.active > a';
          $(selector, context).tab('show');
          //$('.whitebgforproduct').height('auto');
        }
        // Set the correct tab when the page loads
        showTabFromHash(context)
        // Set the correct tab when a user uses their back/forward button
        window.addEventListener('hashchange', showTabFromHash, false);
        // Change the URL when tabs are clicked
        $('a', context).on('click', function(e) {
          history.pushState(null, null, this.href);
        });
        return this;
    };
}( jQuery ));

$(document).ready(function(){
	$('.nav-pills').stickyTabs();
    $('.nav-tabs').stickyTabs();
});