import 'package:flutter/material.dart';

import 'api/client.dart';
import 'models/item.dart';

void main() {
  runApp(const ArmoireApp());
}

class ArmoireApp extends StatelessWidget {
  const ArmoireApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Armoire',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: const WardrobeScreen(),
    );
  }
}

class WardrobeScreen extends StatefulWidget {
  final ApiClient? api;

  const WardrobeScreen({super.key, this.api});

  @override
  State<WardrobeScreen> createState() => _WardrobeScreenState();
}

class _WardrobeScreenState extends State<WardrobeScreen> {
  late final ApiClient _api = widget.api ?? ApiClient();
  late Future<List<Item>> _itemsFuture;

  @override
  void initState() {
    super.initState();
    _itemsFuture = _api.fetchItems();
  }

  void _refresh() {
    setState(() {
      _itemsFuture = _api.fetchItems();
    });
  }

  Future<void> _showAddDialog() async {
    final nameController = TextEditingController();
    String category = 'top';

    final added = await showDialog<bool>(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Add item'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: nameController,
                decoration: const InputDecoration(labelText: 'Name'),
              ),
              DropdownButtonFormField<String>(
                initialValue: category,
                decoration: const InputDecoration(labelText: 'Category'),
                items: const ['top', 'bottom', 'outerwear', 'shoes', 'accessory']
                    .map((c) => DropdownMenuItem(value: c, child: Text(c)))
                    .toList(),
                onChanged: (value) => category = value ?? category,
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context, false),
              child: const Text('Cancel'),
            ),
            FilledButton(
              onPressed: () async {
                if (nameController.text.trim().isEmpty) return;
                await _api.addItem(
                  name: nameController.text.trim(),
                  category: category,
                );
                if (context.mounted) Navigator.pop(context, true);
              },
              child: const Text('Save'),
            ),
          ],
        );
      },
    );

    if (added == true) _refresh();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Wardrobe')),
      floatingActionButton: FloatingActionButton(
        onPressed: _showAddDialog,
        child: const Icon(Icons.add),
      ),
      body: RefreshIndicator(
        onRefresh: () async => _refresh(),
        child: FutureBuilder<List<Item>>(
          future: _itemsFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }
            if (snapshot.hasError) {
              return ListView(
                children: [
                  Padding(
                    padding: const EdgeInsets.all(24),
                    child: Text('Error: ${snapshot.error}'),
                  ),
                ],
              );
            }
            final items = snapshot.data ?? [];
            if (items.isEmpty) {
              return ListView(
                children: const [
                  Padding(
                    padding: EdgeInsets.all(24),
                    child: Text('No items yet. Tap + to add one.'),
                  ),
                ],
              );
            }
            return ListView.builder(
              itemCount: items.length,
              itemBuilder: (context, index) {
                final item = items[index];
                return ListTile(
                  leading: item.imageUrl != null
                      ? Image.network(
                          item.imageUrl!,
                          width: 48,
                          height: 48,
                          fit: BoxFit.cover,
                          errorBuilder: (context, error, stack) =>
                              const Icon(Icons.checkroom),
                        )
                      : const Icon(Icons.checkroom),
                  title: Text(item.name),
                  subtitle: Text([
                    item.category,
                    if (item.brand != null) item.brand,
                    if (item.season != null) item.season,
                    if (item.size != null) item.size,
                  ].whereType<String>().join(' · ')),
                );
              },
            );
          },
        ),
      ),
    );
  }
}
