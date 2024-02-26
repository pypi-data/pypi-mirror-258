from pycognaize.document import Document


if __name__ == '__main__':
    doc = Document.fetch_document(recipe_id="649a7c0180d898001055a354",
                                  doc_id="65db38f7dc54d400119ae1f3")
    doc_text = doc.get_layout_text(
        field_type="output", sorting_function=lambda x: (x.tags[0].top, x.tags[0].left))
    print(doc_text)
    ...
