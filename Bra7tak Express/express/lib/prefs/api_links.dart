class APILinks {
  // static const globalLink = String.fromEnvironment('GLOBAL_LINK',
  //     defaultValue: 'http://127.0.0.1:3030');
  static const globalLink = 'http://192.168.1.4:3030';

  static get login => '$globalLink/webapp/adminstration/login/';
  static get logout => '$globalLink/webapp/adminstration/logout/';
  static get providersData =>
      '$globalLink/webapp/adminstration/shippingInformation/data/';
}
