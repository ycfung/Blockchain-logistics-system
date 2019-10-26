// pages/sign_up/sign_up.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    isAgree: false,
    userId: '',
    stationID: '',
    application: ''
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

  },

  bindAgreeChange: function (e) {
    this.setData({
      isAgree: !!e.detail.value.length
    });
  },

  formSubmit: function (e) {
    console.log('form发生了submit事件，携带数据为：', e.detail.value);
    var formdata = e.detail.value;
    wx.request({
      url: 'http://localhost:8888/MyDemo/Check',
      data: {
        userId: formdata.userId,
        stationID: formdata.stationID,
        application: formdata.application,
        isAgree: this.data.isAgree
      },
      header: { 'content-type': 'application/json' },
      success: function (res) {
        console.log("success!");
        wx.showToast({
          title: '申请已提交',
          icon: 'success',
          duration: 3000
        })
        wx.reLaunch({
          url: '../../pages/index/index',
        })
      },
      fail: function (res) {
        console.log("error!")
      }
    })

  },


  formReset: function () {
    console.log('form发生了reset事件')
  }
})