var VOID_Content = {
    countWords: function () {
      if ($("#totalWordCount").length) {
        var n = 0;
        $.each($("a.archive-title"), function (t, e) {
          n += parseInt($(e).attr("data-words"))
        }), $("#totalWordCount").html(n)
      }
    }, parseTOC: function () {
      if (0 < $(".TOC").length) {
        tocbot.init({
          tocSelector: ".TOC",
          contentSelector: "div[itemprop=articleBody]",
          headingSelector: "h2, h3, h4, h5",
          collapseDepth: 6
        }), $.each($(".toc-link"), function (t, e) {
          $(e).click(function () {
            var t = $(document.getElementById($(this).attr("href").replace("#", ""))).offset().top - 60;
            return $.scrollTo(t, 300), window.innerWidth < 1200 && TOC.close(), !1
          })
        }), 1200 <= window.innerWidth && TOC.open()
      }
    }, parsePhotos: function () {
      $.each($("div[itemprop=articleBody] figure:not(.size-parsed)"), function (t, n) {
        var a = new Image;
        a.src = $(n).find("img").attr("data-src"), a.onload = function () {
          var t = parseFloat(a.width), e = parseFloat(a.height);
          $(n).addClass("size-parsed"), $(n).css("flex-grow", 50 * t / e), $(n).find("a").css("padding-top", e / t * 100 + "%")
        }
      })
    }, parseBoardThumbs: function () {
      $.each($(".board-thumb"), function (t, e) {
        console.log(e)
        VOIDConfig.lazyload ? $(e).html('<img class="lazyload instant" data-src="' + $(e).attr("data-thumb") + '">') : $(e).html('<img src="' + $(e).attr("data-thumb") + '">')
      })
    }, parseUrl: function () {
      var n = document.domain;
      $('a:not(a[href^="#"]):not(".post-like")').each(function (t, e) {
        (!$(e).attr("target") || "" == !$(e).attr("target") && "_self" == !$(e).attr("target")) && e.host != n && $(e).attr("target", "_blank")
      }), VOIDConfig.PJAX && ($.each($('a:not(a[target="_blank"], a[no-pjax])'), function (t, e) {
        e.host == n && $(e).addClass("pjax")
      }), $(document).pjax("a.pjax", {container: "#pjax-container", fragment: "#pjax-container", timeout: 8e3}))
    }, highlight: function () {
      $.each($(".yue pre code"), function (t, e) {
        var n = $(e).attr("class");
        void 0 === n && (n = "language-none"), -1 == n.indexOf("lang") && (n += " language-none"), $(e).attr("class", n)
      }), Prism.highlightAll()
    }, bigfoot: function () {
      $.bigfoot({actionOriginalFN: "ignore"})
    }, pangu: function () {
      pangu.spacingElementByTagName("p")
    }, math: function () {
      VOIDConfig.enableMath && "undefined" != typeof MathJax && (MathJax.Hub.Config({tex2jax: {inlineMath: [["$", "$"], ["\\(", "\\)"]]}}), MathJax.Hub.Queue(["Typeset", MathJax.Hub]))
    }, hyphenate: function () {
      $("div[itemprop=articleBody] p, div[itemprop=articleBody] blockquote").hyphenate("en-us")
    }
  },
  VOID = {
    init: function () {
      VOID_Ui.checkHeader(), VOID_Ui.MasonryCtrler.init(), VOID_Ui.DarkModeSwitcher.checkColorScheme(), VOID_Ui.checkScrollTop(!1), VOID_Content.parseBoardThumbs(), VOID_Ui.lazyload(), VOID_Ui.headroom(), VOID_Content.countWords(), VOID_Content.parseTOC(), VOID_Content.parsePhotos(), VOID_Content.highlight(), VOID_Content.parseUrl(), VOID_Content.pangu(), VOID_Content.bigfoot(), VOID_Content.math(), VOID_Content.hyphenate(), VOID_Vote.reload(), AjaxComment.init(), $("body").on("click", function (t) {
        return VOID_Util.clickIn(t, ".mobile-search-form") || VOID_Util.clickIn(t, "#toggle-mobile-search") || !$(".mobile-search-form").hasClass("opened") ? VOID_Util.clickIn(t, "#toggle-setting-pc") || VOID_Util.clickIn(t, "#toggle-setting") || !$("body").hasClass("setting-panel-show") || VOID_Util.clickIn(t, "#setting-panel") ? void 0 : ($("body").removeClass("setting-panel-show"), setTimeout(function () {
          $("#setting-panel").hide()
        }, 300), !1) : ($(".mobile-search-form").removeClass("opened"), !1)
      })
    }, beforePjax: function () {
      NProgress.start(), VOID_Ui.reset()


    }, afterPjax: function () {
      NProgress.done(), VOID_Content.parseBoardThumbs(),
        VOID_Ui.lazyload(),
      $("#loggin-form").length && $("#loggin-form").addClass("need-refresh"),
        VOID_Ui.MasonryCtrler.init(), VOID_Ui.checkScrollTop(!1), VOID_Content.countWords(),
        VOID_Content.parseTOC(),
        VOID_Content.parsePhotos(),
        VOID_Content.parseUrl(),
        VOID_Content.highlight(),
        VOID_Content.math(),
        VOID_Content.hyphenate(),
        VOID_Content.pangu(),
        VOID_Content.bigfoot(),
        VOID_Vote.reload(), 0 < $(".OwO").length && new OwO({
        logo: "OωO",
        container: document.getElementsByClassName("OwO")[0],
        target: document.getElementsByClassName("input-area")[0],
        api: "/static/VOID/assets/libs/owo/OwO_01.json",
        position: "down",
        width: "400px",
        maxHeight: "250px"
      }), AjaxComment.init()


    }, endPjax: function () {
      $(".TOC").length < 1 && TOC.close()

    }, alert: function (t, e) {
      var n = (new Date).getTime();
      $("body").prepend('<div class="msg" id="msg{id}">{Text}</div>'.replace("{Text}", t).replace("{id}", n)), $.each($(".msg"), function (t, e) {
        $(e).attr("id") != "msg" + n && $(e).css("top", $(e).offset().top - $(document).scrollTop() + $(".msg#msg" + n).outerHeight() + 20 + "px")
      }), $(".msg#msg" + n).addClass("show");
      var a = e;
      "number" != typeof a && (a = 2500), setTimeout(function () {
        $(".msg#msg" + n).addClass("hide"), setTimeout(function () {
          $(".msg#msg" + n).remove()
        }, 1e3)
      }, a)
    }, startSearch: function (t) {
      var e = $(t).val();
      if ($(t).val(""), $(t).blur(), e && "" != e) {
        var n = VOIDConfig.searchBase + e;
        VOIDConfig.PJAX ? $.pjax({
          url: n,
          container: "#pjax-container",
          fragment: "#pjax-container",
          timeout: 8e3
        }) : window.open(n, "_self")
      } else $(t).attr("placeholder", "你还没有输入任何信息")
    }, enterSearch: function (t) {
      13 == (window.event || arguments.callee.caller.arguments[0]).keyCode && VOID.startSearch(t)
    }
  }, VOID_Vote = {
    vote: function (n) {
      var t = $(n).attr("data-type"), a = $(n).attr("data-item-id"), e = $(n).attr("data-table"),
        o = "void_vote_" + e + "_" + t, m = VOID_Util.getCookie(o);
      if (null == m && (m = ","), -1 != m.indexOf("," + a + ",")) return $(n).addClass("done"), void VOID.alert("您已经投过票了~");
      if ($(n).hasClass("comment-vote")) {
        var i = "";
        if (i = "up" == t ? "down" : "up", VOID_Vote.checkVoted(i, a, e)) return void VOID.alert("暂不支持更改投票哦～")
      }
      $.ajax({
        url: VOIDConfig.votePath,
        type: "POST",
        data: JSON.stringify({id: parseInt(a), type: t, choose: e}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (t) {
          switch (200 <= t.code && t.code < 400 && ($(n).addClass("done"), m += a + ",", VOID_Util.setCookie(o, m, 7776e3)), t.code) {
            case 200:
              var e = parseInt($(n).find(".value").text());
              $(n).find(".value").text(e + 1);
              VOID.alert("投票成功～");
              break;
            case 302:
              VOID.alert("您好像已经投过票了呢～");
              break;
            case 403:
              VOID.alert("暂不支持更改投票哦～")
          }
        },
        error: function () {
          VOID.alert("投票失败 o(╥﹏╥)o，请稍后重试")
        }
      })
    }, checkVoted: function (t, e, n) {
      var a = "void_vote_" + n + "_" + t, o = VOID_Util.getCookie(a);
      return null == o && (o = ","), -1 != o.indexOf("," + e + ",")
    }, reload: function () {
      $.each($(".vote-button"), function (t, e) {
        var n = $(e).attr("data-type"), a = $(e).attr("data-item-id"), o = $(e).attr("data-table");
        VOID_Vote.checkVoted(n, a, o) && $(e).addClass("done")
      })
    }, toggleFoldComment: function (t, e) {
      var n = "#comment-" + String(t);
      $(n).toggleClass("fold"), $(n).hasClass("fold") ? $(e).text("点击展开") : $(e).text("还是叠上吧")
    }
  }, Share = {
    parseItem: function (t) {
      return t = $(t).parent(), {
        url: $(t).attr("data-url"),
        title: $(t).attr("data-title"),
        excerpt: $(t).attr("data-excerpt"),
        img: $(t).attr("data-img"),
        twitter: $(t).attr("data-twitter"),
        weibo: $(t).attr("data-weibo")
      }
    }, toWeibo: function (t) {
      var e = Share.parseItem(t),
        n = "http://service.weibo.com/share/share.php?appkey=&title=分享《" + e.title + "》 @" + e.weibo + "%0a%0a" + e.excerpt + "&url=" + e.url + "&pic=" + e.img + "&searchPic=false&style=simple";
      window.open(n)
    }, toTwitter: function (t) {
      var e = Share.parseItem(t),
        n = "https://twitter.com/intent/tweet?text=分享《" + e.title + "》 @" + e.twitter + "%0a%0a" + e.excerpt + "%20" + e.url;
      window.open(n)
    }
  }, AjaxComment = {
    noName: "必须填写用户名",
    noMail: "必须填写电子邮箱地址",
    noContent: "必须填写评论内容",
    invalidMail: "邮箱地址不合法",
    commentsOrder: "DESC",
    commentList: ".comment-list",
    comments: "#comments .comments-title",
    commentReply: ".comment-reply",
    commentForm: "#comment-form",
    respond: ".respond",
    textarea: "#textarea",
    submitBtn: "#submit-button",
    newID: "",
    parentID: "",


    bindClick: function () {
      $(AjaxComment.commentReply + " a, #cancel-comment-reply-link").unbind("click"), $(AjaxComment.commentReply + " a").click(function () {
        AjaxComment.parentID = $(this).parent().parent().parent().attr("id"), $(AjaxComment.textarea).focus()
      }), $("#cancel-comment-reply-link").click(function () {
        AjaxComment.parentID = ""
      })
    },
    err: function () {
      $(AjaxComment.submitBtn).attr("disabled", !1), AjaxComment.newID = ""
    },
    finish: function () {

      TypechoComment.cancelReply(), $(AjaxComment.submitBtn).html("提交评论"), $(AjaxComment.textarea).val(""), $(AjaxComment.submitBtn).attr("disabled", !1), 0 < $("#comment-" + AjaxComment.newID).length && ($.scrollTo($("#comment-" + AjaxComment.newID).offset().top - 50, 500), $("#comment-" + AjaxComment.newID).fadeTo(500, 1)), $(".comment-num .num").html(parseInt($(".comment-num .num").html()) + 1), AjaxComment.bindClick(), VOID_Content.highlight()
    },
    init: function () {
      AjaxComment.bindClick(), $(AjaxComment.commentForm).submit(function () {

        if ($(AjaxComment.submitBtn).attr("disabled", !0), $(AjaxComment.commentForm).find("#author")[0]) {
          if ("" == $(AjaxComment.commentForm).find("#author").val()) return VOID.alert(AjaxComment.noName), AjaxComment.err(), !1;

          if ("" == $(AjaxComment.commentForm).find("#mail").val()) return VOID.alert(AjaxComment.noMail), AjaxComment.err(), !1;
          if (!/^[^@\s<&>]+@([a-z0-9]+\.)+[a-z]{2,4}$/i.test($(AjaxComment.commentForm).find("#mail").val())) return VOID.alert(AjaxComment.invalidMail), AjaxComment.err(), !1
        }


        var t = $(AjaxComment.commentForm).find(AjaxComment.textarea).val().replace(/(^\s*)|(\s*$)/g, "");
        return null == t || "" == t ? (VOID.alert(AjaxComment.noContent), AjaxComment.err()) : ($(AjaxComment.submitBtn).html("提交中"), $.ajax({
          url: $(AjaxComment.commentForm).attr("action"),
          type: $(AjaxComment.commentForm).attr("method"),
          data: $(AjaxComment.commentForm).serializeArray(),
          error: function () {
            return VOID.alert("提交失败！请重试。"), $(AjaxComment.submitBtn).html("提交评论"), AjaxComment.err(), !1
          },
          success: function (t) {
            if (t.code === 200) {
              VOID.alert("评论成功！稍后自动刷新浏览器。");
                  var d = new Date();
                  var re_author = t.data.re_author;
                  var re_mail = t.data.re_mail;
                  var re_url = t.data.re_url;
                  d.setTime(d.getTime() + (24 * 60 * 60 * 7000));
                  var expires = "expires=" + d.toUTCString();
                  document.cookie = 're_author' + "=" + re_author + ";" + expires + ";path=/";
                  document.cookie = 're_mail' + "=" + re_mail + ";" + expires + ";path=/";
                  if (re_url !== ''){
                    document.cookie = 're_url' + "=" + re_url + ";" + expires + ";path=/";
                  }
              setTimeout(function () {
                window.location.reload()
              }, 1000)
            } else {
              return VOID.alert(t.errmsg), $(AjaxComment.submitBtn).html("提交评论"), AjaxComment.err(), !1
            }
          }
        })), !1
      })
    }
  };
$(document).ready(function () {
  VOID.init(), VOIDConfig.PJAX && ($(document).on("pjax:send", function () {
    VOID.beforePjax()
  }), $(document).on("pjax:complete", function () {
    VOID.afterPjax()
  }), $(document).on("pjax:end", function () {
    VOID.endPjax()
  }))
}), window.setInterval(function () {
  var t = (new Date).getTime() - Date.parse(VOIDConfig.buildTime);
  t = Math.floor(t / 1e3);
  var e = Math.floor(t / 86400);
  t %= 86400;
  var n = Math.floor(t / 3600);
  t %= 3600;
  var a = Math.floor(t / 60);
  t %= 60;
  var o = Math.floor(t / 1);
  $("#uptime").html(e + " 天 " + n + " 小时 " + a + " 分 " + o + " 秒 ")
}, 1e3);



function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Setting the token on the AJAX request
$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
  }
});