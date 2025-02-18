from magelang.runtime import Punctuated, CharStream, EOF


from .cst import *


def parse_close_brace(stream: CharStream) -> MagedownCloseBrace | None:
    buffer = ''
    field = stream.peek()
    if not (field == '}'):
        return
    stream.get()
    buffer += field
    return MagedownCloseBrace()


def parse_open_brace_slash(stream: CharStream) -> MagedownOpenBraceSlash | None:
    buffer = ''
    field = stream.peek()
    if not (field == '{'):
        return
    stream.get()
    field = stream.peek()
    if not (field == '/'):
        return
    stream.get()
    buffer += field
    return MagedownOpenBraceSlash()


def parse_open_brace(stream: CharStream) -> MagedownOpenBrace | None:
    buffer = ''
    field = stream.peek()
    if not (field == '{'):
        return
    stream.get()
    buffer += field
    return MagedownOpenBrace()


def parse_reject_keyword(stream: CharStream) -> MagedownRejectKeyword | None:
    buffer = ''
    field = stream.peek()
    if not (field == 'r'):
        return
    stream.get()
    field = stream.peek()
    if not (field == 'e'):
        return
    stream.get()
    field = stream.peek()
    if not (field == 'j'):
        return
    stream.get()
    field = stream.peek()
    if not (field == 'e'):
        return
    stream.get()
    field = stream.peek()
    if not (field == 'c'):
        return
    stream.get()
    field = stream.peek()
    if not (field == 't'):
        return
    stream.get()
    buffer += field
    return MagedownRejectKeyword()


def parse_accept_keyword(stream: CharStream) -> MagedownAcceptKeyword | None:
    buffer = ''
    field = stream.peek()
    if not (field == 'a'):
        return
    stream.get()
    field = stream.peek()
    if not (field == 'c'):
        return
    stream.get()
    field = stream.peek()
    if not (field == 'c'):
        return
    stream.get()
    field = stream.peek()
    if not (field == 'e'):
        return
    stream.get()
    field = stream.peek()
    if not (field == 'p'):
        return
    stream.get()
    field = stream.peek()
    if not (field == 't'):
        return
    stream.get()
    buffer += field
    return MagedownAcceptKeyword()


def parse_backtick_backtick_backtick(stream: CharStream) -> MagedownBacktickBacktickBacktick | None:
    buffer = ''
    field = stream.peek()
    if not (field == '`'):
        return
    stream.get()
    field = stream.peek()
    if not (field == '`'):
        return
    stream.get()
    field = stream.peek()
    if not (field == '`'):
        return
    stream.get()
    buffer += field
    return MagedownBacktickBacktickBacktick()


def parse_backtick(stream: CharStream) -> MagedownBacktick | None:
    buffer = ''
    field = stream.peek()
    if not (field == '`'):
        return
    stream.get()
    buffer += field
    return MagedownBacktick()


def parse_close_bracket_close_bracket(stream: CharStream) -> MagedownCloseBracketCloseBracket | None:
    buffer = ''
    field = stream.peek()
    if not (field == ']'):
        return
    stream.get()
    field = stream.peek()
    if not (field == ']'):
        return
    stream.get()
    buffer += field
    return MagedownCloseBracketCloseBracket()


def parse_close_bracket(stream: CharStream) -> MagedownCloseBracket | None:
    buffer = ''
    field = stream.peek()
    if not (field == ']'):
        return
    stream.get()
    buffer += field
    return MagedownCloseBracket()


def parse_open_bracket_open_bracket(stream: CharStream) -> MagedownOpenBracketOpenBracket | None:
    buffer = ''
    field = stream.peek()
    if not (field == '['):
        return
    stream.get()
    field = stream.peek()
    if not (field == '['):
        return
    stream.get()
    buffer += field
    return MagedownOpenBracketOpenBracket()


def parse_open_bracket(stream: CharStream) -> MagedownOpenBracket | None:
    buffer = ''
    field = stream.peek()
    if not (field == '['):
        return
    stream.get()
    buffer += field
    return MagedownOpenBracket()


def parse_close_paren(stream: CharStream) -> MagedownCloseParen | None:
    buffer = ''
    field = stream.peek()
    if not (field == ')'):
        return
    stream.get()
    buffer += field
    return MagedownCloseParen()


def parse_open_paren(stream: CharStream) -> MagedownOpenParen | None:
    buffer = ''
    field = stream.peek()
    if not (field == '('):
        return
    stream.get()
    buffer += field
    return MagedownOpenParen()


def parse_hashtag(stream: CharStream) -> MagedownHashtag | None:
    buffer = ''
    field = stream.peek()
    if not (field == '#'):
        return
    stream.get()
    buffer += field
    return MagedownHashtag()


def parse_line_feed(stream: CharStream) -> MagedownLineFeed | None:
    buffer = ''
    field = stream.peek()
    if not (field == '\n'):
        return
    stream.get()
    buffer += field
    return MagedownLineFeed()


def parse_name(stream: CharStream) -> MagedownName | None:
    field = stream.peek()
    if not (((field >= 'a') and (field <= 'z')) or ((field >= 'A') and (field <= 'Z'))):
        return
    stream.get()
    field_1 = ''
    while True:
        stream_1 = stream.fork()
        field_1_element = stream_1.peek()
        if not ((field_1_element == '_') or ((field_1_element >= 'a') and (field_1_element <= 'z')) or ((field_1_element >= '0') and (field_1_element <= '9')) or ((field_1_element >= 'A') and (field_1_element <= 'Z'))):
            break
        else:
            stream_1.get()
            stream.join_to(stream_1)
            field_1 += field_1_element
    return MagedownName(field=field, field_1=field_1)


def parse_code_block(stream: CharStream) -> MagedownCodeBlock | None:
    backtick_backtick_backtick = parse_backtick_backtick_backtick(stream)
    if backtick_backtick_backtick is None:
        return
    lang = None
    stream_3 = stream.fork()
    temp_tuple_0 = parse_name(stream_3)
    if not (temp_tuple_0 is None):
        temp_unused = stream_3.peek()
        if (temp_unused == '\t') or (temp_unused == '\r') or (temp_unused == '\n') or (temp_unused == ' '):
            stream_3.get()
            temp = temp_tuple_0
            lang = temp
            stream.join_to(stream_3)
    text = ''
    while True:
        stream_1 = stream.fork()
        stream_2 = stream_1.fork()
        text_element_unused = parse_backtick_backtick_backtick(stream_2)
        if not (text_element_unused is None):
            break
        else:
            text_element_tuple_1 = stream_1.peek()
            if not ((text_element_tuple_1 >= '\x00') and (text_element_tuple_1 <= '\x7f')):
                break
            else:
                stream_1.get()
                text_element = text_element_tuple_1
                stream.join_to(stream_1)
                text += text_element
    backtick_backtick_backtick_2 = parse_backtick_backtick_backtick(stream)
    if backtick_backtick_backtick_2 is None:
        return
    return MagedownCodeBlock(backtick_backtick_backtick=backtick_backtick_backtick, lang=lang, text=text, backtick_backtick_backtick_2=backtick_backtick_backtick_2)


def parse_inline_code(stream: CharStream) -> MagedownInlineCode | None:
    backtick = parse_backtick(stream)
    if backtick is None:
        return
    text = ''
    while True:
        stream_1 = stream.fork()
        stream_2 = stream_1.fork()
        text_element_unused = parse_backtick(stream_2)
        if not (text_element_unused is None):
            break
        else:
            text_element_tuple_1 = stream_1.peek()
            if not ((text_element_tuple_1 >= '\x00') and (text_element_tuple_1 <= '\x7f')):
                break
            else:
                stream_1.get()
                text_element = text_element_tuple_1
                stream.join_to(stream_1)
                text += text_element
    backtick_2 = parse_backtick(stream)
    if backtick_2 is None:
        return
    return MagedownInlineCode(backtick=backtick, text=text, backtick_2=backtick_2)


def parse_heading(stream: CharStream) -> MagedownHeading | None:
    hashtags = []
    hashtags_element = parse_hashtag(stream)
    if hashtags_element is None:
        return
    hashtags.append(hashtags_element)
    while True:
        stream_5 = stream.fork()
        hashtags_element = parse_hashtag(stream_5)
        if hashtags_element is None:
            break
        else:
            stream.join_to(stream_5)
            hashtags.append(hashtags_element)
    text = ''
    stream_4 = stream.fork()
    text_element_unused_1 = parse_line_feed(stream_4)
    if not (text_element_unused_1 is None):
        return
    text_element_tuple_1_1 = stream.peek()
    if not ((text_element_tuple_1_1 >= '\x00') and (text_element_tuple_1_1 <= '\x7f')):
        return
    stream.get()
    text_element = text_element_tuple_1_1
    text += text_element
    while True:
        stream_2 = stream.fork()
        stream_3 = stream_2.fork()
        text_element_unused = parse_line_feed(stream_3)
        if not (text_element_unused is None):
            break
        else:
            text_element_tuple_1 = stream_2.peek()
            if not ((text_element_tuple_1 >= '\x00') and (text_element_tuple_1 <= '\x7f')):
                break
            else:
                stream_2.get()
                text_element = text_element_tuple_1
                stream.join_to(stream_2)
                text += text_element
    match = False
    stream_1 = stream.fork()
    temp = parse_line_feed(stream_1)
    if not (temp is None):
        stream.join_to(stream_1)
        match = True
    else:
        stream_1 = stream.fork()
        c_1 = stream_1.peek()
        if c_1 == EOF:
            stream.join_to(stream_1)
            match = True
    if not match:
        return
    return MagedownHeading(hashtags=hashtags, text=text)


def parse_ref(stream: CharStream) -> MagedownRef | None:
    open_bracket_open_bracket = parse_open_bracket_open_bracket(stream)
    if open_bracket_open_bracket is None:
        return
    name = parse_name(stream)
    if name is None:
        return
    close_bracket_close_bracket = parse_close_bracket_close_bracket(stream)
    if close_bracket_close_bracket is None:
        return
    return MagedownRef(open_bracket_open_bracket=open_bracket_open_bracket, name=name, close_bracket_close_bracket=close_bracket_close_bracket)


def parse_link(stream: CharStream) -> MagedownLink | None:
    open_bracket = parse_open_bracket(stream)
    if open_bracket is None:
        return
    text = ''
    while True:
        stream_3 = stream.fork()
        stream_4 = stream_3.fork()
        text_element_unused = parse_close_bracket(stream_4)
        if not (text_element_unused is None):
            break
        else:
            text_element_tuple_1 = stream_3.peek()
            if not ((text_element_tuple_1 >= '\x00') and (text_element_tuple_1 <= '\x7f')):
                break
            else:
                stream_3.get()
                text_element = text_element_tuple_1
                stream.join_to(stream_3)
                text += text_element
    close_bracket = parse_close_bracket(stream)
    if close_bracket is None:
        return
    open_paren = parse_open_paren(stream)
    if open_paren is None:
        return
    href = ''
    while True:
        stream_1 = stream.fork()
        stream_2 = stream_1.fork()
        href_element_unused = parse_close_paren(stream_2)
        if not (href_element_unused is None):
            break
        else:
            href_element_tuple_1 = stream_1.peek()
            if not ((href_element_tuple_1 >= '\x00') and (href_element_tuple_1 <= '\x7f')):
                break
            else:
                stream_1.get()
                href_element = href_element_tuple_1
                stream.join_to(stream_1)
                href += href_element
    close_paren = parse_close_paren(stream)
    if close_paren is None:
        return
    return MagedownLink(open_bracket=open_bracket, text=text, close_bracket=close_bracket, open_paren=open_paren, href=href, close_paren=close_paren)


def parse_accepts(stream: CharStream) -> MagedownAccepts | None:
    open_brace = parse_open_brace(stream)
    if open_brace is None:
        return
    accept_keyword = parse_accept_keyword(stream)
    if accept_keyword is None:
        return
    close_brace = parse_close_brace(stream)
    if close_brace is None:
        return
    text = ''
    while True:
        stream_1 = stream.fork()
        stream_2 = stream_1.fork()
        text_element_unused_tuple_0 = parse_open_brace_slash(stream_2)
        if text_element_unused_tuple_0 is None:
            text_element_tuple_1 = stream_1.peek()
            if not ((text_element_tuple_1 >= '\x00') and (text_element_tuple_1 <= '\x7f')):
                break
            else:
                stream_1.get()
                text_element = text_element_tuple_1
                stream.join_to(stream_1)
                text += text_element
        else:
            text_element_unused_tuple_1 = parse_accept_keyword(stream_2)
            if text_element_unused_tuple_1 is None:
                text_element_tuple_1 = stream_1.peek()
                if not ((text_element_tuple_1 >= '\x00') and (text_element_tuple_1 <= '\x7f')):
                    break
                else:
                    stream_1.get()
                    text_element = text_element_tuple_1
                    stream.join_to(stream_1)
                    text += text_element
            else:
                text_element_unused_tuple_2 = parse_close_brace(stream_2)
                if not (text_element_unused_tuple_2 is None):
                    text_element_unused = (text_element_unused_tuple_0, text_element_unused_tuple_1, text_element_unused_tuple_2)
                    break
                else:
                    text_element_tuple_1 = stream_1.peek()
                    if not ((text_element_tuple_1 >= '\x00') and (text_element_tuple_1 <= '\x7f')):
                        break
                    else:
                        stream_1.get()
                        text_element = text_element_tuple_1
                        stream.join_to(stream_1)
                        text += text_element
    open_brace_slash = parse_open_brace_slash(stream)
    if open_brace_slash is None:
        return
    accept_keyword_2 = parse_accept_keyword(stream)
    if accept_keyword_2 is None:
        return
    close_brace_2 = parse_close_brace(stream)
    if close_brace_2 is None:
        return
    return MagedownAccepts(open_brace=open_brace, accept_keyword=accept_keyword, close_brace=close_brace, text=text, open_brace_slash=open_brace_slash, accept_keyword_2=accept_keyword_2, close_brace_2=close_brace_2)


def parse_rejects(stream: CharStream) -> MagedownRejects | None:
    open_brace = parse_open_brace(stream)
    if open_brace is None:
        return
    reject_keyword = parse_reject_keyword(stream)
    if reject_keyword is None:
        return
    close_brace = parse_close_brace(stream)
    if close_brace is None:
        return
    text = ''
    while True:
        stream_1 = stream.fork()
        stream_2 = stream_1.fork()
        text_element_unused_tuple_0 = parse_open_brace_slash(stream_2)
        if text_element_unused_tuple_0 is None:
            text_element_tuple_1 = stream_1.peek()
            if not ((text_element_tuple_1 >= '\x00') and (text_element_tuple_1 <= '\x7f')):
                break
            else:
                stream_1.get()
                text_element = text_element_tuple_1
                stream.join_to(stream_1)
                text += text_element
        else:
            text_element_unused_tuple_1 = parse_reject_keyword(stream_2)
            if text_element_unused_tuple_1 is None:
                text_element_tuple_1 = stream_1.peek()
                if not ((text_element_tuple_1 >= '\x00') and (text_element_tuple_1 <= '\x7f')):
                    break
                else:
                    stream_1.get()
                    text_element = text_element_tuple_1
                    stream.join_to(stream_1)
                    text += text_element
            else:
                text_element_unused_tuple_2 = parse_close_brace(stream_2)
                if not (text_element_unused_tuple_2 is None):
                    text_element_unused = (text_element_unused_tuple_0, text_element_unused_tuple_1, text_element_unused_tuple_2)
                    break
                else:
                    text_element_tuple_1 = stream_1.peek()
                    if not ((text_element_tuple_1 >= '\x00') and (text_element_tuple_1 <= '\x7f')):
                        break
                    else:
                        stream_1.get()
                        text_element = text_element_tuple_1
                        stream.join_to(stream_1)
                        text += text_element
    open_brace_slash = parse_open_brace_slash(stream)
    if open_brace_slash is None:
        return
    reject_keyword_2 = parse_reject_keyword(stream)
    if reject_keyword_2 is None:
        return
    close_brace_2 = parse_close_brace(stream)
    if close_brace_2 is None:
        return
    return MagedownRejects(open_brace=open_brace, reject_keyword=reject_keyword, close_brace=close_brace, text=text, open_brace_slash=open_brace_slash, reject_keyword_2=reject_keyword_2, close_brace_2=close_brace_2)


def parse_special(stream: CharStream) -> MagedownSpecial | None:
    match = False
    stream_1 = stream.fork()
    result = parse_code_block(stream_1)
    if not (result is None):
        stream.join_to(stream_1)
        match = True
    else:
        stream_1 = stream.fork()
        result = parse_inline_code(stream_1)
        if not (result is None):
            stream.join_to(stream_1)
            match = True
        else:
            stream_1 = stream.fork()
            result = parse_heading(stream_1)
            if not (result is None):
                stream.join_to(stream_1)
                match = True
            else:
                stream_1 = stream.fork()
                result = parse_ref(stream_1)
                if not (result is None):
                    stream.join_to(stream_1)
                    match = True
                else:
                    stream_1 = stream.fork()
                    result = parse_link(stream_1)
                    if not (result is None):
                        stream.join_to(stream_1)
                        match = True
                    else:
                        stream_1 = stream.fork()
                        result = parse_accepts(stream_1)
                        if not (result is None):
                            stream.join_to(stream_1)
                            match = True
                        else:
                            stream_1 = stream.fork()
                            result = parse_rejects(stream_1)
                            if not (result is None):
                                stream.join_to(stream_1)
                                match = True
    if not match:
        return
    return result


def parse_text(stream: CharStream) -> MagedownText | None:
    contents = ''
    stream_3 = stream.fork()
    contents_element_unused_1 = parse_special(stream_3)
    if not (contents_element_unused_1 is None):
        return
    contents_element_tuple_1_1 = stream.peek()
    if not ((contents_element_tuple_1_1 >= '\x00') and (contents_element_tuple_1_1 <= '\x7f')):
        return
    stream.get()
    contents_element = contents_element_tuple_1_1
    contents += contents_element
    while True:
        stream_1 = stream.fork()
        stream_2 = stream_1.fork()
        contents_element_unused = parse_special(stream_2)
        if not (contents_element_unused is None):
            break
        else:
            contents_element_tuple_1 = stream_1.peek()
            if not ((contents_element_tuple_1 >= '\x00') and (contents_element_tuple_1 <= '\x7f')):
                break
            else:
                stream_1.get()
                contents_element = contents_element_tuple_1
                stream.join_to(stream_1)
                contents += contents_element
    return MagedownText(contents=contents)


def parse_document(stream: CharStream) -> MagedownDocument | None:
    elements = []
    while True:
        stream_1 = stream.fork()
        match = False
        stream_2 = stream_1.fork()
        elements_element = parse_text(stream_2)
        if not (elements_element is None):
            stream_1.join_to(stream_2)
            match = True
        else:
            stream_2 = stream_1.fork()
            elements_element = parse_special(stream_2)
            if not (elements_element is None):
                stream_1.join_to(stream_2)
                match = True
        if not match:
            break
        else:
            stream.join_to(stream_1)
            elements.append(elements_element)
    return MagedownDocument(elements=elements)


def parse_token(stream: CharStream) -> MagedownToken | None:
    match = False
    stream_1 = stream.fork()
    result = parse_accept_keyword(stream_1)
    if not (result is None):
        stream.join_to(stream_1)
        match = True
    else:
        stream_1 = stream.fork()
        result = parse_reject_keyword(stream_1)
        if not (result is None):
            stream.join_to(stream_1)
            match = True
    if not match:
        return
    return result


def parse_node(stream: CharStream) -> MagedownNode | None:
    match = False
    stream_1 = stream.fork()
    result = parse_name(stream_1)
    if not (result is None):
        stream.join_to(stream_1)
        match = True
    else:
        stream_1 = stream.fork()
        result = parse_code_block(stream_1)
        if not (result is None):
            stream.join_to(stream_1)
            match = True
        else:
            stream_1 = stream.fork()
            result = parse_inline_code(stream_1)
            if not (result is None):
                stream.join_to(stream_1)
                match = True
            else:
                stream_1 = stream.fork()
                result = parse_heading(stream_1)
                if not (result is None):
                    stream.join_to(stream_1)
                    match = True
                else:
                    stream_1 = stream.fork()
                    result = parse_ref(stream_1)
                    if not (result is None):
                        stream.join_to(stream_1)
                        match = True
                    else:
                        stream_1 = stream.fork()
                        result = parse_link(stream_1)
                        if not (result is None):
                            stream.join_to(stream_1)
                            match = True
                        else:
                            stream_1 = stream.fork()
                            result = parse_accepts(stream_1)
                            if not (result is None):
                                stream.join_to(stream_1)
                                match = True
                            else:
                                stream_1 = stream.fork()
                                result = parse_rejects(stream_1)
                                if not (result is None):
                                    stream.join_to(stream_1)
                                    match = True
                                else:
                                    stream_1 = stream.fork()
                                    result = parse_text(stream_1)
                                    if not (result is None):
                                        stream.join_to(stream_1)
                                        match = True
                                    else:
                                        stream_1 = stream.fork()
                                        result = parse_document(stream_1)
                                        if not (result is None):
                                            stream.join_to(stream_1)
                                            match = True
    if not match:
        return
    return result


def parse_syntax(stream: CharStream) -> MagedownSyntax | None:
    match = False
    stream_1 = stream.fork()
    result = parse_token(stream_1)
    if not (result is None):
        stream.join_to(stream_1)
        match = True
    else:
        stream_1 = stream.fork()
        result = parse_node(stream_1)
        if not (result is None):
            stream.join_to(stream_1)
            match = True
    if not match:
        return
    return result


