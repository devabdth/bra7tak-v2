import 'dart:convert';

import 'package:express/prefs/api_links.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart';

class ShippingProvidersController with ChangeNotifier, DiagnosticableTreeMixin {
  Future<Map<String, dynamic>?> getAllProviders() async {
    try {
      final res = await get(Uri.parse(APILinks.providersData));
      if (res.statusCode != 200) return null;
      var data = jsonDecode(res.body);
      data = Map<String, dynamic>.from(data);
      return data;
    } catch (e) {
      return {};
    }
  }
}
