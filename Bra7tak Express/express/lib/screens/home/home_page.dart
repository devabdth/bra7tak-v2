import 'package:express/prefs/theme.dart';
import 'package:express/screens/order_status/order_status.dart';
import 'package:express/screens/providers/shipping_providers.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final _fieldController = TextEditingController();
  late List<Map> options, baseOptions;
  @override
  void initState() {
    super.initState();
    baseOptions = [
      {
        'title': 'Change Order Status',
        'icon': 'assets/status.png',
        'target': const OrderStatusScanner(),
      },
      {
        'title': 'Assign Order to Shipping Company',
        'icon': 'assets/shipping.png',
        'target': const ShippingProviderScanner(),
      }
    ];
    options = baseOptions;
  }

  @override
  Widget build(BuildContext context) {
    final mq = MediaQuery.of(context);
    return Scaffold(
      backgroundColor: AppTheme.background,
      body: SingleChildScrollView(
        child: SizedBox(
          width: mq.size.width,
          height: mq.size.height,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              SizedBox(
                width: mq.size.width,
                height: mq.size.height * 0.275,
                child: Stack(
                  children: [
                    Container(
                      height: mq.size.width * 0.5,
                      width: mq.size.width,
                      decoration: const BoxDecoration(
                        color: AppTheme.primaryColor,
                        borderRadius: BorderRadius.only(
                          bottomLeft: Radius.circular(50),
                          bottomRight: Radius.circular(50),
                        ),
                      ),
                      child: Padding(
                        padding: EdgeInsets.only(
                          left: 16,
                          right: 16,
                          top: mq.size.width * 0.15,
                        ),
                        child: Text(
                          'Welcome Back!',
                          style: TextStyle(
                            color: AppTheme.background,
                            fontWeight: FontWeight.w500,
                            fontFamily: AppTheme.primaryFontFamily,
                            fontStyle: FontStyle.italic,
                            fontSize: mq.size.width * 0.075,
                          ),
                        ),
                      ),
                    ),
                    Positioned(
                      bottom: 0,
                      left: 0,
                      right: 0,
                      child: Center(
                        child: Container(
                          height: mq.size.width * 0.15,
                          width: mq.size.width * 0.9,
                          decoration: BoxDecoration(
                            color: AppTheme.backgroundVarient,
                            borderRadius: BorderRadius.circular(10),
                            boxShadow: <BoxShadow>[
                              BoxShadow(
                                color: Colors.black.withOpacity(0.5),
                                offset: Offset(0, mq.size.height * 0.01),
                                blurRadius: 30,
                                spreadRadius: 1,
                              ),
                            ],
                          ),
                          child: Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 16),
                            child: Center(
                              child: TextField(
                                controller: _fieldController,
                                onChanged: (_) {
                                  setState(() {
                                    options = baseOptions
                                        .where((element) => element['title']
                                            .toLowerCase()
                                            .contains(_fieldController.text
                                                .trim()
                                                .toLowerCase()))
                                        .toList();
                                  });
                                },
                                decoration: const InputDecoration(
                                  border: InputBorder.none,
                                  errorBorder: InputBorder.none,
                                  enabledBorder: InputBorder.none,
                                  disabledBorder: InputBorder.none,
                                  focusedBorder: InputBorder.none,
                                  focusedErrorBorder: InputBorder.none,
                                  hintText: 'Search Option, etc...',
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),
                    )
                  ],
                ),
              ),
              SizedBox(height: mq.size.width * 0.05),
              for (var option in options) ...[
                SizedBox(height: mq.size.width * 0.025),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: GestureDetector(
                    onTap: () {
                      Get.to(option['target']);
                    },
                    child: Container(
                        width: double.infinity,
                        height: mq.size.width * 0.15,
                        decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(12),
                            color: Colors.white,
                            boxShadow: const <BoxShadow>[
                              BoxShadow(
                                offset: Offset.zero,
                                spreadRadius: 10,
                                blurRadius: 5,
                                color: Colors.black12,
                              )
                            ]),
                        child: Padding(
                          padding: const EdgeInsets.symmetric(
                              vertical: 8, horizontal: 16),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Container(
                                width: mq.size.width * 0.1,
                                height: mq.size.width * 0.1,
                                decoration: BoxDecoration(
                                    image: DecorationImage(
                                  image: AssetImage(option['icon']),
                                  fit: BoxFit.contain,
                                  repeat: ImageRepeat.noRepeat,
                                  alignment: Alignment.center,
                                )),
                              ),
                              SizedBox(width: mq.size.width * 0.05),
                              Text(
                                option['title'],
                                style: TextStyle(
                                  fontSize: mq.size.width * 0.035,
                                  color: Colors.black,
                                  fontWeight: FontWeight.w700,
                                  fontFamily: 'Raleway',
                                ),
                              ),
                            ],
                          ),
                        )),
                  ),
                ),
                SizedBox(height: mq.size.width * 0.05),
              ],
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Container(
                    width: double.infinity,
                    height: mq.size.width * 0.15,
                    decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(12),
                        color: Colors.white,
                        boxShadow: const <BoxShadow>[
                          BoxShadow(
                            offset: Offset.zero,
                            spreadRadius: 10,
                            blurRadius: 5,
                            color: Colors.black12,
                          )
                        ]),
                    child: Padding(
                      padding: const EdgeInsets.symmetric(
                          vertical: 8, horizontal: 16),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          SizedBox(
                            width: mq.size.width * 0.1,
                            height: mq.size.width * 0.1,
                          ),
                          SizedBox(width: mq.size.width * 0.05),
                          Text(
                            'TBA',
                            style: TextStyle(
                              fontSize: mq.size.width * 0.035,
                              color: Colors.black,
                              fontWeight: FontWeight.w700,
                              fontFamily: 'Raleway',
                            ),
                          ),
                        ],
                      ),
                    )),
              )
            ],
          ),
        ),
      ),
    );
  }
}
