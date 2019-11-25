const app = getApp()
Page({
  data: {
    /** 
     * 用于控制当 scroll-view 滚动到底部时，显示 “数据加载中...” 的提示 
     */
    hidden: true,
    /** 
     * 用于显示文章的数组 
     */
    articles: [],
    /** 
     * 数据是否正在加载中，避免用户瞬间多次下滑到底部，发生多次数据加载事件 
     */
    loadingData: false
  },
  onLoad: function (options) {
    this.loadData(true);
  },
  loadData: function (tail, callback) {
    var that = this;
    wx.request({
      url: 'https://www.csdn.net/api/articles?type=more&category=home&shown_offset=0',
      data:{
      notify:"",//获取交易市场上所有的请求

      },
      success: function (r) {
        // var oldArticles = that.data.articles,
        //   newArticles = tail ? oldArticles.concat(r.data.articles) : r.data.articles.concat(oldArticles);
        that.setData({
          articles: r.data.articles
        });
        if (callback) {
          callback();
        }
      },
      error: function (r) {
        console.info('error', r);
      },
      complete: function () { }
    })
  },
  /** 
   * 上滑加载更多 
   */
  scrollToLower: function (e) {
    console.info('scrollToLower', e);
    var hidden = this.data.hidden,
      loadingData = this.data.loadingData,
      that = this;
    if (hidden) {
      this.setData({
        hidden: false
      });
      console.info(this.data.hidden);
    }
    if (loadingData) {
      return;
    }
    this.setData({
      loadingData: true
    });
    // 加载数据,模拟耗时操作  

    wx.showLoading({
      title: '数据加载中...',
    });

    setTimeout(function () {
      that.loadData(true, () => {
        that.setData({
          hidden: true,
          loadingData: false
        });
        wx.hideLoading();
      });
      console.info('上拉数据加载完成.');
    }, 2000);
  },
  scrollToUpper: function (e) {
    wx.showToast({
      title: '触顶了...',
    })
  },
  sure:function(e){
    var that = this;
    wx.request({
      url: 'https://www.csdn.net/api/articles?type=more&category=home&shown_offset=0',
      data: {
        notify: "",//接受某个订单
        order_number: e.detail.value.pnumber

      },
      success: function (r) {
        // var oldArticles = that.data.articles,
        //   newArticles = tail ? oldArticles.concat(r.data.articles) : r.data.articles.concat(oldArticles);
  wx.navigateTo({
    url: '../success/success',
  })
      },
      error: function (r) {
        console.info('error', r);
      },
      complete: function () { }
    })
  }
})