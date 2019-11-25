// pages/order_details/order_details.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    hidden:false,
    articles: [],
    loadingData: false

  },

  /**
   * 生命周期函数--监听页面加载
   */

  onLoad: function (options) {
    this.loadData(true);

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  loadData: function (tail, callback) {
    var that = this;
    wx.request({
      url: 'https://www.csdn.net/api/articles?type=more&category=home&shown_offset=0',
      data: {
        notify: "",//代表获取我提出的正在运行请求有关的信息
      },
      success: function (r) {
        var oldArticles = that.data.articles,
          newArticles = tail ? oldArticles.concat(r.data.articles) : r.data.articles.concat(oldArticles);
        that.setData({
          articles: newArticles
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
  sure: function (e) {

    var that = this;
    wx.request({
      url: 'https://www.csdn.net/api/articles?type=more&category=home&shown_offset=0',
      data: {
        notify: "",//自己取货
        order_number: this.articles[e.detail.value.index].pnumber
      },
      success: function (r) {
        wx.navigateTo({
          url: '../success/success',
        })
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
  }
})