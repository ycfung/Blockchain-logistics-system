// pages/in/in.js
var app = getApp();
var util = require('../../utils/util.js');

Page({

  /**
   * 页面的初始数据
   */
  data: {
    pNumber: '',
    phone: '',
    inDate: null,
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

  formSubmit: function (e) {
    console.log('form发生了submit事件，携带数据为：', e.detail.value);
    var formdata = e.detail.value;
    if (formdata.packet_number == "" || formdata.phone_number == ""){
      wx.showToast({
        title: '信息不能为空',
      })
    }else{
    var DATE = util.formatDate(new Date());
    wx.request({
      url: 'http://localhost:8888/MyDemo/Check',
      data: {
        pNumber : formdata.pNumber,
        phone : formdata.phone,
        inDate : DATE,
      },
      header: { 'content-type': 'application/json' },
      success: function (res) {
        console.log("success!");
        wx.showToast({
          title: '已完成',
          icon: 'success',
          duration: 3000
        })
      },
      fail: function (res) {
        console.log("error!")
      }
    })
    }
  },

  formReset: function () {
    console.log('form发生了reset事件')
  }
})