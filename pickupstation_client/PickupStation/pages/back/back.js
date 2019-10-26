// pages/back/back.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    backList:[]
  },

  onLoad: function (options) {
    this.loadData();
  },


  loadData: function () {
    var that = this;
    wx.showLoading()
    wx.request({
      url: 'http://localhost:8888/MyDemo/',
      method: 'GET',
      header: { 'content-type': 'application/json' },
      success: function (res) {
        that.setData({
          backList: res.data.backList
        })
        console.log(res.data);
        wx.showToast({ title: '数据加载完成' })
      },
      fail: function (res) {
        wx.showToast({ title: '数据加载失败' })
      }
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

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

  }
})