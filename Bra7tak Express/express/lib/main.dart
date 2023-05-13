import 'package:express/providers/login.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:express/screens/login/login_page.dart';
import 'package:get_storage/get_storage.dart';
import 'package:get/get.dart';

import 'providers/shipping_providers.dart';

void main() {
  GetStorage.init();
  runApp(const Bra7takExpress());
}

class Bra7takExpress extends StatelessWidget {
  const Bra7takExpress({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => LoginProvider()),
        ChangeNotifierProvider(create: (_) => ShippingProvidersController()),
      ],
      child: const GetMaterialApp(
        home: LoginPage(),
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}
