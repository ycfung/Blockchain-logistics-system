// pages/new_order/new_order.js
const app = getApp();
var QQMapWX = require('../../map/qqmap-wx-jssdk.js');

// 实例化API核心类
var qqmapsdk = new QQMapWX({
  key: 'EEYBZ-CSQ64-LKDU3-DH4EO-UCABV-INBUY' // 必填
});

Page({

  /**
   * 页面的初始数据
   */
  data: {
    from_position: "",
    to_position: "",
    date:"2016-09-01",
    index: 0,
    time:"09:01",
    weight: ["1kg", "2kg", "3kg", "4kg", "5kg", "6kg", "7kg", "8kg", "9kg", "10kg", "11kg", "12kg", "13kg", "14kg", "15kg", "16kg", "17kg", "18kg", "19kg", "20kg", "21kg", "22kg", "23kg", "24kg", "25kg", "26kg", "27kg", "28kg", "29kg", "30kg", "31kg", "32kg", "33kg", "34kg", "35kg", "36kg", "37kg", "38kg", "39kg", "40kg"],
    weightIndex: 0,
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
  //事件处理函数
  bindTimeChange: function (e) {
    this.setData({
      time: e.detail.value
    });
  },
  bindPickerChange: function (e) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      index: e.detail.value
    })
  },
  //向服务器发送请求
  formSubmit: function (e) {
    var that = this;
    var formData = e.detail.value;
    if (e.detail.value.cost == '' || e.detail.value.from_position == '' || e.detail.value.to_position == '' || e.detail.value.weight == '' || e.detail.value.time == '' || e.detail.value.credentials == '' || e.detail.value.date == '') {
      wx.showToast({
        title: '请填写完整···',
      })
    } else {
      wx.request({
        url: 'http://101.132.96.109:8000/',//这里的接口请填实际接口     
        data: {
          notify: 5,
          key: wx.getStorageSync('key'),
          formData

        },

        header: {
          'Content-Type': 'application/json'
        },
        //这里设置成功的返回信息
        success: function (res) {
          console.log(res.data)
          that.setData({
            form_info: ''
          })
        }
      })
    }

  },

  loadData: function (tail, callback) {

  },
  bindDateChange: function (e) {
    this.setData({
      date: e.detail.value
    })
  },
  bindTimeChange: function (e) {
    this.setData({
      time: e.detail.value
    })
  },
  bindCountryChange: function (e) {
    console.log('picker country 发生选择改变，携带值为', e.detail.value);

    this.setData({
      weightIndex: e.detail.value
    })
  },
  
})