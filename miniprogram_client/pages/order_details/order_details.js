// pages/order_details/order_details.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    open1: false,
    open2:false,
    open3: false,
    articles: [],
    articles1: [],
    articles2: [],
    loadingData: false

  },

  /**
   * 生命周期函数--监听页面加载
   */
  showitem1: function () {
    this.setData({
      open1: !this.data.open1
    })
  },
  showitem2: function () {
    this.setData({
      open2: !this.data.open2
    })
  },
  showitem3: function () {
    this.setData({
      open3: !this.data.open3
    })
  },

  onLoad: function (options) {
    this.loadData1(true);
    this.loadData2(true);
    this.loadData3(true);
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
  loadData1: function (tail, callback) {
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
  loadData2: function (tail, callback) {
    var that = this;
    wx.request({
      url: 'https://www.csdn.net/api/articles?type=more&category=home&shown_offset=0',
      data: {
        notify: "",//代表获取我接单正在运行的有关的信息
      },
      success: function (r) {
        var oldArticles = that.data.articles1,
          newArticles = tail ? oldArticles.concat(r.data.articles1) : r.data.articles1.concat(oldArticles);
        that.setData({
          articles1: newArticles
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
  loadData3: function (tail, callback) {
    var that = this;
    wx.request({
      url: 'https://www.csdn.net/api/articles?type=more&category=home&shown_offset=0',
      data: {
        notify: "",//获取在快递点没有任何操作的快递信息
      },
      success: function (r) {
        var oldArticles = that.data.articles2,
          newArticles = tail ? oldArticles.concat(r.data.articles2) : r.data.articles2.concat(oldArticles);
        that.setData({
          articles2: newArticles
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
Confirm_goods:function(e){

  var that = this;
  wx.request({
    url: 'https://www.csdn.net/api/articles?type=more&category=home&shown_offset=0',
    data: {
      notify: "",//确认收货
      order_number: e.detail.value.order_number
    },
    success: function (r) {
//成功
    },
    error: function (r) {
      console.info('error', r);
    },
    complete: function () { }
  })

},
  pickUp:function(e){
    var that = this;
    wx.request({
      url: 'https://www.csdn.net/api/articles?type=more&category=home&shown_offset=0',
      data: {
        notify: "",//自己取快递
        order_number: e.detail.value.order_number
      },
      success: function (r) {
        //成功
      },
      error: function (r) {
        console.info('error', r);
      },
      complete: function () { }
    }) 
  },
  entrust:function(e){
  wx.navigateTo({
    url: '../new_order/new_order',
  })
  },
  Confirm_delivery:function(e)
  {
    var that = this;
    wx.request({
      url: 'https://www.csdn.net/api/articles?type=more&category=home&shown_offset=0',
      data: {
        notify: "",//确认快递送达
        order_number: e.detail.value.order_number
      },
      success: function (r) {
        //成功
      },
      error: function (r) {
        console.info('error', r);
      },
      complete: function () { }
    }) 
  }
})