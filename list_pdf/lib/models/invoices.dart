import 'dart:async';
import 'dart:convert';

import 'package:list_pdf/models/invoices.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:list_pdf/firebase_options.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:list_pdf/download_button.dart';

class Invoice {
  final String title;
  final String desc;
  final String url;

  const Invoice({
    required this.title,
    required this.desc,
    required this.url,
  });

  factory Invoice.fromJson(Map<String, dynamic> json) {
    return Invoice(
      title: json['Name'] as String,
      desc: json['Description'] as String,
      url: json['link'] as String,
    );
  }
}

Future<List<Invoice>> fetchInvoices(http.Client client) async {
  final response = await http.get(
      Uri.parse('http://127.0.0.1:5000/api/getAllRecords'),
      headers: {"Access-Control-Allow-Origin": "*"});

  // Use the compute function to run parsePhotos in a separate isolate.
  return compute(parseInvoices, response.body);
}

// A function that converts a response body into a List<Photo>.
List<Invoice> parseInvoices(String responseBody) {
  final parsed = jsonDecode(responseBody).cast<Map<String, dynamic>>();

  return parsed.map<Invoice>((json) => Invoice.fromJson(json)).toList();
}
