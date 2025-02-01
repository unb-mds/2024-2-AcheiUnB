export default class Item {
  constructor(
    user = null,
    name = "",
    category = "",
    location = "",
    color = "",
    found_lost_date = "",
    brand = "",
    description = null,
    images = null,
    status = "",
    barcode = "",
    requiredFields = ["name", "category", "location"],
  ) {
    this.user = user;
    this.name = name;
    this.category = category;
    this.location = location;
    this.color = color;
    this.brand = brand;
    this.description = description;
    this.images = images;
    this.status = status;
    this.found_lost_date = found_lost_date;
    this.barcode = barcode;
    this.requiredFields = requiredFields;
  }
}
