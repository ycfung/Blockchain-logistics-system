// pages/out/out.js
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    show: '',
    pNumber: '',
    msg: undefined,
    permission: app.globalData.permission
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
      pNumber: ""
    });
  },

  formSubmit: function (e) {
    var formdata = e.detail.value;
    if (formdata.pNumber == ""){
      wx.showToast({
        title: '货单号不能为空',
      })
    }else{
    var that = this;
    wx.request({
      url: 'http://localhost:8888/MyDemo/Check',
      method: 'GET',
      header: { 'content-type': 'application/json' },
      data:{
        pNumber: formdata.pNumber
      },
      success: function (res) {
        that.setData({
          msg: res.data.msg
        })
        if(that.data.msg == true){
          wx.showToast({ title: "出库成功！"})
        }else{
          wx.showToast({ title: "货物已被取走，请重新核对！" })
        }
        that.clearInput();
      },
      fail: function (res) {
        console.log("error!")
      }
    })
    }
  }

})