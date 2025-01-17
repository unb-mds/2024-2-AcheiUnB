export default class FormModel {
  constructor(entity) {
    this.entity = entity;
  }

  validate() {
    for (const requiredFieldKey of this.entity.requiredFields) {
      const field = this.entity[requiredFieldKey];
      if (!field || field === "") {
        console.log(`Erro: O campo '${requiredFieldKey}' é obrigatório.`);
        return false;
      }
    }

    console.log("Formula´rio válido");
    return true;
  }

  toFormData() {
    const formData = new FormData();

    for (const [key, value] of Object.entries(this.entity)) {
      if (key !== "requiredFields" && value !== undefined && value !== null) {
        if (Array.isArray(value)) {
          value.forEach((elemento, index) => {
            formData.append(`${key}[${index}]`, elemento);
          });
        } else {
          formData.append(key, value);
        }
      }
    }

    console.log("Formulário criado:");
    return formData;
  }

  setFieldValue(field, value) {
    this.entity[field] = value;
  }
}