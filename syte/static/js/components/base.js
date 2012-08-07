// Global configs and functions shared between js
// Require.js configs
require.config({
  paths: {
    "text": "js/libs/text",
    "json": "js/libs/json",
  },
  optimizeAllPluginResources: true,
  preserveLicenseComments: false,
  inlineText: true,
  inlineJSON: false,
});

// Spin.js configs
var spin_opts = {
  lines: 9,
  length: 5,
  width: 2,
  radius: 4,
  rotate: 9,
  color: '#4c4c4c',
  speed: 1.5,
  trail: 40,
  shadow: false,
  hwaccel: false,
  className: 'spinner',
  zIndex: 2e9
};

// index.html --- Load blog posts
require(["jquery", "js/components/blog-posts", "js/libs/jquery.url", "json"],
  function() {
    $(function() {
      if (typeof indexPage === 'undefined' || !indexPage) {
        return
      }

      if (tagSlug) {
        fetchBlogPosts(postOffset, tagSlug);
      } else {
        fetchBlogPosts(postOffset);
      }
      if (disqus_integration_enabled) {
        $('body').bind('blog-post-loaded', function() {
          embedDisqus(true);
        });
      }
    });

    var resultsLoaded = false;
    $(window).scroll(function() {
      if (!resultsLoaded && ($(window).scrollTop() + $(window).height() > $(document).height()/1.2)) {
        resultsLoaded = true;
        postOffset += 20;
        if (tagSlug) {
          fetchBlogPosts(postOffset, tagSlug);
        } else {
          fetchBlogPosts(postOffset);
        }
      }
      if (resultsLoaded && ($(window).scrollTop() + $(window).height() < $(document).height()/1.2)) {
        resultsLoaded = false;
      }
    });
  }
);

// blog-posts.html --- load a single blog post
require(["jquery", "js/components/links", "js/components/blog-posts"],
  function(base) {
    $(function() {
      if (typeof blogsPage === 'undefined' || !blogsPage) {
        return
      }

      setupLinks();
      adjustBlogHeaders();

      if (disqus_integration_enabled) {
        embedDisqus();
      }
    });
  }
);

function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
