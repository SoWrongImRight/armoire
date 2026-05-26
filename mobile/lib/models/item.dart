class Item {
  final int id;
  final String name;
  final String category;
  final String? brand;
  final String? season;
  final String? size;
  final String? imageUrl;

  Item({
    required this.id,
    required this.name,
    required this.category,
    this.brand,
    this.season,
    this.size,
    this.imageUrl,
  });

  factory Item.fromJson(Map<String, dynamic> json) {
    return Item(
      id: json['id'] as int,
      name: json['name'] as String,
      category: json['category'] as String,
      brand: json['brand'] as String?,
      season: json['season'] as String?,
      size: json['size'] as String?,
      imageUrl: json['image_url'] as String?,
    );
  }
}
