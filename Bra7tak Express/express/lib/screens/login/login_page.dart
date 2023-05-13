import 'package:express/prefs/theme.dart';
import 'package:express/providers/login.dart';
import 'package:express/screens/home/home_page.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:provider/provider.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({Key? key}) : super(key: key);

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final emailControllor = TextEditingController();
  final emailFocusNode = FocusNode();
  final passcodeControllor = TextEditingController();
  final passcodeFocusNode = FocusNode();

  late String msg;
  late bool isLoading;
  @override
  void initState() {
    msg = '';
    isLoading = false;
    super.initState();
  }

  @override
  void dispose() {
    emailControllor.dispose();
    passcodeControllor.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final _loginProvider = context.watch<LoginProvider>();
    final mq = MediaQuery.of(context);
    return Scaffold(
      backgroundColor: AppTheme.background,
      body: SingleChildScrollView(
        child: SizedBox(
          width: mq.size.width,
          height: mq.size.height,
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                RichText(
                  text: TextSpan(
                    children: <InlineSpan>[
                      TextSpan(
                        text: 'Bra7tak ',
                        style: TextStyle(
                          fontFamily: AppTheme.primaryFontFamily,
                          color: AppTheme.primaryColor,
                          fontWeight: FontWeight.w900,
                          fontSize: mq.size.width * 0.065,
                        ),
                      ),
                      TextSpan(
                        text: 'Express',
                        style: TextStyle(
                          fontFamily: AppTheme.secondaryFontFamily,
                          fontStyle: FontStyle.italic,
                          color: AppTheme.primaryColor,
                          fontWeight: FontWeight.w300,
                          fontSize: mq.size.width * 0.065,
                        ),
                      ),
                    ],
                  ),
                ),
                SizedBox(height: mq.size.height * 0.05),
                TextField(
                  decoration: InputDecoration(
                    border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15),
                        borderSide: const BorderSide(
                            color: AppTheme.secondaryVarientColor, width: 1)),
                    errorBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15),
                        borderSide: const BorderSide(
                            color: AppTheme.secondaryVarientColor, width: 1)),
                    enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15),
                        borderSide: const BorderSide(
                            color: AppTheme.secondaryVarientColor, width: 1)),
                    focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15),
                        borderSide: const BorderSide(
                            color: AppTheme.secondaryVarientColor, width: 1)),
                    disabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15),
                        borderSide: const BorderSide(
                            color: AppTheme.secondaryVarientColor, width: 1)),
                    focusedErrorBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15),
                        borderSide: const BorderSide(
                            color: AppTheme.secondaryVarientColor, width: 1)),
                    hintText: 'Username',
                    hintStyle: TextStyle(
                      fontStyle: FontStyle.italic,
                      fontFamily: AppTheme.secondaryFontFamily,
                      color: AppTheme.secondaryColor,
                      fontSize: mq.size.width * 0.035,
                    ),
                  ),
                  focusNode: emailFocusNode,
                  controller: emailControllor,
                ),
                SizedBox(height: mq.size.height * 0.05),
                TextField(
                  obscureText: true,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15),
                        borderSide: const BorderSide(
                            color: AppTheme.secondaryVarientColor, width: 1)),
                    errorBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15),
                        borderSide: const BorderSide(
                            color: AppTheme.secondaryVarientColor, width: 1)),
                    enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15),
                        borderSide: const BorderSide(
                            color: AppTheme.secondaryVarientColor, width: 1)),
                    focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15),
                        borderSide: const BorderSide(
                            color: AppTheme.secondaryVarientColor, width: 1)),
                    disabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15),
                        borderSide: const BorderSide(
                            color: AppTheme.secondaryVarientColor, width: 1)),
                    focusedErrorBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(15),
                        borderSide: const BorderSide(
                            color: AppTheme.secondaryVarientColor, width: 1)),
                    hintText: 'Passcode',
                    hintStyle: TextStyle(
                      fontStyle: FontStyle.italic,
                      fontFamily: AppTheme.secondaryFontFamily,
                      color: AppTheme.secondaryColor,
                      fontSize: mq.size.width * 0.035,
                    ),
                  ),
                  controller: passcodeControllor,
                  focusNode: passcodeFocusNode,
                ),
                SizedBox(height: mq.size.height * 0.025),
                Text(
                  msg,
                  style: TextStyle(
                    color: AppTheme.secondaryVarientColor,
                    fontSize: mq.size.width * 0.035,
                    fontFamily: AppTheme.secondaryFontFamily,
                  ),
                ),
                SizedBox(height: mq.size.height * 0.05),
                TextButton(
                  onPressed: isLoading
                      ? () {}
                      : () async {
                          final email = emailControllor.text.trim();
                          final passcode = passcodeControllor.text.trim();
                          if (email.isEmpty || email.length < 4) {
                            setState(() {
                              msg = 'Please Enter a valid username';
                            });
                            return;
                          }
                          if (passcode.isEmpty || passcode.length < 4) {
                            setState(() {
                              msg = 'Please Enter a valid Passcode';
                            });
                            return;
                          }
                          setState(() {
                            isLoading = true;
                          });
                          final bool res = await _loginProvider.login(
                              username: email, passcode: passcode);
                          if (res) {
                            Get.to(const HomePage());
                            return;
                          }
                          setState(() {
                            isLoading = false;
                          });
                          msg = 'Failed to loggin, Try again later!';
                        },
                  child: Container(
                    width: mq.size.width * 0.5,
                    height: mq.size.height * 0.08,
                    decoration: BoxDecoration(
                      color: AppTheme.primaryColor,
                      borderRadius: BorderRadius.circular(25),
                    ),
                    child: isLoading
                        ? const Center(
                            child: CircularProgressIndicator(
                              color: AppTheme.background,
                            ),
                          )
                        : Center(
                            child: Text(
                              'Submit',
                              style: TextStyle(
                                color: AppTheme.background,
                                fontSize: mq.size.width * 0.045,
                                fontFamily: AppTheme.primaryFontFamily,
                              ),
                            ),
                          ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
