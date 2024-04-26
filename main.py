from parse_hh import get_ingo_cards_pages, write_contacts_to_csv


def main():
    info_card = get_ingo_cards_pages(num_page=1)
    write_contacts_to_csv(info_card, 'asd')


if __name__ == '__main__':
    main()
