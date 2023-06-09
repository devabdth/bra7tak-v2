import 'dart:convert';
import 'dart:developer';

import 'package:app/prefs/api_links.dart';
import 'package:flutter/material.dart';
import 'package:get_storage/get_storage.dart';
import 'package:http/http.dart';

class LoginProvider extends ChangeNotifier {
  final String storageToken = 'CURRENT_ADMN_ID';
  late bool loggedIn;
  late String? currentLoggedInUserId;

  LoginProvider() {
    currentLoggedInUserId = GetStorage().read(storageToken);
    loggedIn = currentLoggedInUserId == null;
  }

  static bool get isLoggedIn => GetStorage().read('CURRENT_ADMN_ID') == null;

  Future<bool> login(
      {required String username, required String passcode}) async {
    try {
      final res = await patch(Uri.parse(APILinks.login),
          body: json.encode({'username': username, 'accessKey': passcode}));
      if (res.statusCode == 200) return Future.value(true);

      return Future.value(false);
    } catch (e) {
      log(e.toString());
      return Future.value(false);
    }
  }

  Future<bool> logout() async {
    try {
      final res = await get(Uri.parse(APILinks.logout));
      if (res.statusCode == 200) return Future.value(true);

      return Future.value(false);
    } catch (e) {
      log(e.toString());
      return Future.value(false);
    }
  }
}
