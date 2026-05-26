import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/item.dart';

/// Base URL of the Armoire backend.
///
/// Defaults to the Android emulator's host alias (10.0.2.2). Override with:
///   flutter run --dart-define=API_BASE_URL=http://localhost:8000
const String apiBaseUrl = String.fromEnvironment(
  'API_BASE_URL',
  defaultValue: 'http://10.0.2.2:8000',
);

class ApiClient {
  final String baseUrl;
  final http.Client _http;

  ApiClient({String? baseUrl, http.Client? client})
      : baseUrl = baseUrl ?? apiBaseUrl,
        _http = client ?? http.Client();

  Future<List<Item>> fetchItems() async {
    final res = await _http.get(Uri.parse('$baseUrl/items'));
    if (res.statusCode != 200) {
      throw Exception('Failed to load items (${res.statusCode})');
    }
    final data = jsonDecode(res.body) as List<dynamic>;
    return data
        .map((e) => Item.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<Item> addItem({required String name, required String category}) async {
    final res = await _http.post(
      Uri.parse('$baseUrl/items'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'name': name, 'category': category}),
    );
    if (res.statusCode != 201) {
      throw Exception('Failed to add item (${res.statusCode})');
    }
    return Item.fromJson(jsonDecode(res.body) as Map<String, dynamic>);
  }
}
