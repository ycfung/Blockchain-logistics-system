//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: '',
    userInfo: {},
    hasUserInfo: false,
    haslogin:app.globalData.haslogin,
    permission: app.globalData.permission,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
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
    //当逻辑执行完后关闭刷新    
    wx.stopPullDownRefresh()
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

  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },

  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
    if (app.globalData.haslogin){
      this.AuthorCheck();
    }
  },

  AuthorCheck: function () {
    /** 快递点权限检验*/

    var that = this
    wx.request({
      url: 'http://localhost:8888/MyDemo/Check',
      headers: {
        'Content-Type': 'application/json'
      },
      data: {
        id: app.globalData.id
      },
      success: function (res) {
        //将获取到的json数据，存在
        app.globalData.permission = res.data.permission;
        that.setData({
          permission: res.data.permission,
          //res代表success函数的事件对，data是固定的
        })
        console.log(res.data);
        console.log(app.globalData.permission);
        if (!app.globalData.permission) {
          that.setData({
            motto: '未认证'
          })
          wx.showModal({
            title: '快递点未验证',
            content: '您还未通过权限认证，如果还未申请，请先前往提交注册申请；如果已申请，请耐心等待',
            confirmText: "前往申请",
            cancelText: "等待认证",
            success: function (res) {
              console.log(res);
              if (res.confirm) {
                console.log('用户提交权限申请')
                wx.navigateTo({
                  url: '/pages/sign_up/sign_up',
                })
              } else {
                console.log('用户等待')
                wx.navigateTo({
                  url:'/pages/index/index',
                })
              }
            }
          });
        }
        else {
          that.setData({
            motto: '已认证'
          })
        }  
        console.log('success!');
      },
      fail: function (res) {
        console.log('error!');
      },
    })
  },

  login: function(e) {
    var formdata = e.detail.value;
    if (formdata.id == ""||formdata.pwd=="") {
      wx.showToast({
        title: 'ID或密码不能为空',
      })
    } else {
      var that = this;
      wx.request({
        url: 'http://localhost:8888/MyDemo/Login',
        method: 'GET',
        header: { 'content-type': 'application/json' },
        data: {
          id: formdata.id,
          pwd: formdata.pwd
        },
        success: function (res) {
          console.log(res)
          if (res.data.msg == true) {
            wx.showToast({ title: "登录成功！" })
            app.globalData.id = formdata.id;
            app.globalData.haslogin = true;
            that.setData({
              haslogin: true
            })
            console.log("haslogin = ", app.globalData.haslogin )
            that.onLoad();
            that.onShow();
          } else {
            wx.showToast({ title: "ID或密码错误！" })
          }
        },
        fail: function (res) {
          console.log("error!")
        }
      })
    }
  },


  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  }
})
