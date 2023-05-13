import 'package:express/prefs/theme.dart';
import 'package:express/providers/shipping_providers.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class ShippingProviderScanner extends StatefulWidget {
  const ShippingProviderScanner({Key? key}) : super(key: key);

  @override
  State<ShippingProviderScanner> createState() =>
      _ShippingProviderScannerState();
}

class _ShippingProviderScannerState extends State<ShippingProviderScanner> {
  late List<String> orders;
  @override
  void initState() {
    super.initState();
    orders = [
      "sdfsdfsdfsdcsdcsdfsdfsfsdf1",
      "sdfsdfsdfsdcsdcsdfsdfsfsdf2",
      "sdfsdfsdfsdcsdcsdfsdfsfsdf3",
      "sdfsdfsdfsdcsdcsdfsdfsfsdf4",
      "sdfsdfsdfsdcsdcsdfsdfsfsdf5",
      "sdfsdfsdfsdcsdcsdfsdfsfsdf6",
      "sdfsdfsdfsdcsdcsdfsdfsfsdf7",
    ];
  }

  String? currentShippingProvider;
  @override
  Widget build(BuildContext context) {
    final _shippingProvidersController =
        context.watch<ShippingProvidersController>();
    final mq = MediaQuery.of(context);
    return FutureBuilder<Map?>(
        future: _shippingProvidersController.getAllProviders(),
        builder: (context, snapshot) {
          print(snapshot.data);
          if (!(snapshot.hasData)) {
            return Scaffold(
              backgroundColor: AppTheme.background,
              appBar: AppBar(
                backgroundColor: AppTheme.primaryColor,
                leadingWidth: mq.size.width * 0.1,
                title: Text(
                  'Shipping Providers Scanner',
                  style: TextStyle(
                    color: Colors.white,
                    fontFamily: 'Raleway',
                    fontSize: mq.size.width * 0.05,
                  ),
                ),
              ),
              body: const Center(
                child: CircularProgressIndicator(
                  color: AppTheme.primaryColor,
                ),
              ),
            );
          }
          final Map providers = snapshot.data!;
          return Scaffold(
            backgroundColor: AppTheme.background,
            appBar: AppBar(
              backgroundColor: AppTheme.primaryColor,
              leadingWidth: mq.size.width * 0.1,
              title: Text(
                'Shipping Providers Scanner',
                style: TextStyle(
                  color: Colors.white,
                  fontFamily: 'Raleway',
                  fontSize: mq.size.width * 0.05,
                ),
              ),
            ),
            body: SingleChildScrollView(
              child: Padding(
                padding:
                    const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (orders.isEmpty) ...[
                      Text(
                        'Select Provider',
                        style: TextStyle(
                          color: Colors.black,
                          fontWeight: FontWeight.w700,
                          fontFamily: 'Raleway',
                          fontSize: mq.size.width * 0.045,
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.symmetric(
                            vertical: 8, horizontal: 16),
                        child: DropdownButton<Map>(
                            isExpanded: true,
                            isDense: true,
                            underline: Container(),
                            value: currentShippingProvider == null
                                ? providers.values.first
                                : providers.values
                                    .toList()
                                    .where((element) =>
                                        element['id'] ==
                                        currentShippingProvider)
                                    .first,
                            items: providers.values
                                .map((value) => DropdownMenuItem<Map>(
                                      value: value,
                                      child: Text(value['name']),
                                    ))
                                .toList(),
                            onChanged: (v) {
                              setState(() {
                                currentShippingProvider = v!['id'];
                              });
                            }),
                      ),
                      SizedBox(height: mq.size.height * 0.1),
                    ],
                    Text(
                      'Orders (${orders.length})',
                      style: TextStyle(
                        color: Colors.black,
                        fontWeight: FontWeight.w700,
                        fontFamily: 'Raleway',
                        fontSize: mq.size.width * 0.045,
                      ),
                    ),
                    SizedBox(height: mq.size.width * 0.025),
                    Container(
                      width: mq.size.width,
                      constraints: BoxConstraints(
                        minWidth: double.infinity,
                        maxWidth: double.infinity,
                        maxHeight: mq.size.height * 5,
                        minHeight: mq.size.height * 0.3,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.symmetric(
                            vertical: 8, horizontal: 16),
                        child: SingleChildScrollView(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: orders
                                .map((order) => Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.spaceBetween,
                                      crossAxisAlignment:
                                          CrossAxisAlignment.center,
                                      children: [
                                        Text(order),
                                        TextButton(
                                          onPressed: () {
                                            orders.remove(order);
                                            setState(() {});
                                          },
                                          child: Text(
                                            'x',
                                            style: TextStyle(
                                              color: Colors.red,
                                              fontFamily: 'Raleway',
                                              fontSize: mq.size.width * 0.025,
                                            ),
                                          ),
                                        )
                                      ],
                                    ))
                                .toList(),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            bottomNavigationBar: Container(
              width: double.infinity,
              height: mq.size.width * 0.2,
              child: Padding(
                padding:
                    const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    TextButton(
                      onPressed: () {
                        setState(() {
                          orders = [];
                        });
                      },
                      child: SizedBox(
                        width: mq.size.width * 0.2,
                        height: double.infinity,
                        child: Center(
                          child: Text(
                            'Clear',
                            style: TextStyle(
                              color: AppTheme.primaryColor,
                              fontSize: mq.size.width * 0.045,
                              fontFamily: AppTheme.primaryFontFamily,
                            ),
                          ),
                        ),
                      ),
                    ),
                    TextButton(
                      onPressed: () {},
                      child: Container(
                        width: mq.size.width * 0.6,
                        height: double.infinity,
                        decoration: BoxDecoration(
                          color: AppTheme.primaryColor,
                          borderRadius: BorderRadius.circular(25),
                        ),
                        child: Center(
                          child: Text(
                            'Scan',
                            style: TextStyle(
                              color: AppTheme.background,
                              fontSize: mq.size.width * 0.045,
                              fontFamily: AppTheme.primaryFontFamily,
                            ),
                          ),
                        ),
                      ),
                    )
                  ],
                ),
              ),
            ),
          );
        });
  }
}
