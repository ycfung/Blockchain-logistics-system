// pages/return/return.js
Page({

  /**
   * 页面的初始数据
   */
  data: {

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

  clearInput: function () {
    this.setData({
      inputVal: ""
    });
  },
  input: function (e) {
    this.setData({
      pNumber: e.data.value
    });
  },
  return: function () {
    if (this.data.pNumber == "") {
      wx.showToast({
        title: '货单号不能为空',
      })
    } else {
      var that = this;
      wx.request({
        url: 'http://localhosat:8888/MyDemo/',
        method: 'GET',
        header: { 'content-type': 'application/json' },
        data: {
          pNumber,
        },
        success: function (res) {
          that.setData({
            msg: res.data.msg
          })
          if (this.data.msg == true) {
            wx.showToast({ title: "退还成功！" })
          } else {
            wx.showToast({ title: "快递未逾期走，请等待！" })
          }
          this.clearInput();
        },
        fail: function (res) {
          console.log("error!")
        }
      })
    }
  },

  history:function(){
    wx.navigateTo({
      url:'../../pages/back/back'
    })
  }

})