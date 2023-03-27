import 'package:express/prefs/theme.dart';
import 'package:flutter/material.dart';

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
        // 'navigation': OrderStatusScanner(),
      },
      {
        'title': 'Assign Order to Shipping Company',
        'icon': 'assets/shipping.png',
        // 'navigation': OrderStatusScanner(),
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
              for (var option in options) ...[
                SizedBox(height: mq.size.width * 0.025),
                Text(option['title']),
                SizedBox(height: mq.size.width * 0.025),
              ]
            ],
          ),
        ),
      ),
    );
  }
}
