import 'package:armoire_mobile/api/client.dart';
import 'package:armoire_mobile/main.dart';
import 'package:armoire_mobile/models/item.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';

void main() {
  test('Item.fromJson parses API payload', () {
    final item = Item.fromJson({
      'id': 1,
      'name': 'Blue Shirt',
      'category': 'top',
      'brand': 'Uniqlo',
      'season': 'all',
      'size': 'M',
      'image_url': 'http://example/img.png',
    });
    expect(item.id, 1);
    expect(item.name, 'Blue Shirt');
    expect(item.imageUrl, 'http://example/img.png');
  });

  testWidgets('WardrobeScreen renders items from the API', (tester) async {
    final mockHttp = MockClient((request) async {
      return http.Response(
        '[{"id":1,"name":"Blue Shirt","category":"top","brand":null,'
        '"season":null,"size":null,"image_url":null}]',
        200,
        headers: {'content-type': 'application/json'},
      );
    });

    await tester.pumpWidget(
      MaterialApp(home: WardrobeScreen(api: ApiClient(client: mockHttp))),
    );
    await tester.pumpAndSettle();

    expect(find.text('Blue Shirt'), findsOneWidget);
  });
}
