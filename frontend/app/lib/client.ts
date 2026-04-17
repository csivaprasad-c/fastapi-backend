/* eslint-disable */
/* tslint:disable */
// @ts-nocheck
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/** TagName */
export enum TagName {
  EXPRESS = "EXPRESS",
  STANDARD = "STANDARD",
  FRAGILE = "FRAGILE",
  HEAVY = "HEAVY",
  INTERNATIONAL = "INTERNATIONAL",
  DOMESTIC = "DOMESTIC",
  TEMPERATURE_CONTROLLED = "TEMPERATURE_CONTROLLED",
  GIFT = "GIFT",
  RETURN = "RETURN",
  DOCUMENTS = "DOCUMENTS",
}

/** ShipmentStatus */
export enum ShipmentStatus {
  Placed = "placed",
  InTransit = "in_transit",
  Delivered = "delivered",
  OutForDelivery = "out_for_delivery",
  Cancelled = "cancelled",
}

/** Body_login_delivery_partner */
export interface BodyLoginDeliveryPartner {
  /** Grant Type */
  grant_type?: string | null;
  /** Username */
  username: string;
  /**
   * Password
   * @format password
   */
  password: string;
  /**
   * Scope
   * @default ""
   */
  scope?: string;
  /** Client Id */
  client_id?: string | null;
  /**
   * Client Secret
   * @format password
   */
  client_secret?: string | null;
}

/** Body_login_seller */
export interface BodyLoginSeller {
  /** Grant Type */
  grant_type?: string | null;
  /** Username */
  username: string;
  /**
   * Password
   * @format password
   */
  password: string;
  /**
   * Scope
   * @default ""
   */
  scope?: string;
  /** Client Id */
  client_id?: string | null;
  /**
   * Client Secret
   * @format password
   */
  client_secret?: string | null;
}

/** Body_reset_password */
export interface BodyResetPassword {
  /** Password */
  password: string;
}

/** Body_submit_review */
export interface BodySubmitReview {
  /**
   * Rating
   * @min 1
   * @max 5
   */
  rating: number;
  /** Comment */
  comment: string | null;
}

/** CreateDeliveryPartner */
export interface CreateDeliveryPartner {
  /**
   * Name
   * @maxLength 30
   */
  name: string;
  /**
   * Email
   * @format email
   * @maxLength 50
   */
  email: string;
  /** Max Handling Capacity */
  max_handling_capacity: number;
  /** Password */
  password: string;
  /** Serviceable Zip Codes */
  serviceable_zip_codes: number[];
}

/** CreateSeller */
export interface CreateSeller {
  /**
   * Name
   * @maxLength 30
   */
  name: string;
  /**
   * Email
   * @format email
   * @maxLength 50
   */
  email: string;
  /** Password */
  password: string;
  /** Address */
  address: string;
  /** Zip Code */
  zip_code: number;
}

/** HTTPValidationError */
export interface HTTPValidationError {
  /** Detail */
  detail?: ValidationError[];
}

/** ReadDeliveryPartner */
export interface ReadDeliveryPartner {
  /**
   * Name
   * @maxLength 30
   */
  name: string;
  /**
   * Email
   * @format email
   * @maxLength 50
   */
  email: string;
  /** Max Handling Capacity */
  max_handling_capacity: number;
  /**
   * Id
   * @format uuid
   */
  id: string;
}

/** ReadSeller */
export interface ReadSeller {
  /**
   * Name
   * @maxLength 30
   */
  name: string;
  /**
   * Email
   * @format email
   * @maxLength 50
   */
  email: string;
  /**
   * Id
   * @format uuid
   */
  id: string;
}

/** Seller */
export interface Seller {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
  /**
   * Email Verified
   * @default false
   */
  email_verified?: boolean;
  /**
   * Id
   * @format uuid
   */
  id?: string;
  /**
   * Created At
   * @format date-time
   */
  created_at: string;
  /** Address */
  address?: string | null;
  /** Zip Code */
  zip_code?: number | null;
}

/**
 * ShipmentCreate
 * Shipment details to create a new shipment.
 */
export interface ShipmentCreate {
  /**
   * Content
   * @maxLength 30
   */
  content: string;
  /**
   * Weight
   * Weight must be less than 25 kg
   * @max 25
   */
  weight: number;
  /**
   * Destination
   * ZIP code of the destination
   */
  destination: number;
  /**
   * Tags
   * List of tags associated with the shipment
   */
  tags?: Tag[];
  /**
   * Client Contact Email
   * @format email
   */
  client_contact_email: string;
  /** Client Contact Phone */
  client_contact_phone?: string | null;
}

/** ShipmentEvent */
export interface ShipmentEvent {
  /**
   * Id
   * @format uuid
   */
  id?: string;
  /**
   * Created At
   * @format date-time
   */
  created_at: string;
  /** Location */
  location: number;
  status: ShipmentStatus;
  /** Description */
  description?: string | null;
  /**
   * Shipment Id
   * @format uuid
   */
  shipment_id: string;
}

/** ShipmentPatch */
export interface ShipmentPatch {
  /** Content */
  content?: string | null;
  /**
   * Weight
   * Weight must be less than 25 kg
   */
  weight?: number | null;
  /** Destination */
  destination?: number | null;
  status?: ShipmentStatus | null;
}

/** ShipmentRead */
export interface ShipmentRead {
  /**
   * Content
   * @maxLength 30
   */
  content: string;
  /**
   * Weight
   * Weight must be less than 25 kg
   * @max 25
   */
  weight: number;
  /**
   * Destination
   * ZIP code of the destination
   */
  destination: number;
  /** Tags */
  tags: TagRead[];
  /**
   * Id
   * @format uuid
   */
  id: string;
  /**
   * Estimated Delivery
   * @format date-time
   */
  estimated_delivery: string;
  seller: Seller;
  /** Timeline */
  timeline: ShipmentEvent[];
}

/** ShipmentUpdate */
export interface ShipmentUpdate {
  /** Location */
  location?: number | null;
  status?: ShipmentStatus | null;
  /** Description */
  description?: string | null;
  /** Estimated Delivery */
  estimated_delivery?: string | null;
  /** Verification Code */
  verification_code?: number | null;
}

/** Tag */
export interface Tag {
  /**
   * Id
   * @format uuid
   */
  id?: string;
  name: TagName;
  /** Instruction */
  instruction: string;
}

/** TagRead */
export interface TagRead {
  name: TagName;
  /** Instruction */
  instruction: string;
}

/** TokenData */
export interface TokenData {
  /** Access Token */
  access_token: string;
  /** Token Type */
  token_type: string;
}

/** UpdateDeliveryPartner */
export interface UpdateDeliveryPartner {
  /** Serviceable Zip Codes */
  serviceable_zip_codes?: number[] | null;
  /** Max Handling Capacity */
  max_handling_capacity?: number | null;
}

/** ValidationError */
export interface ValidationError {
  /** Location */
  loc: (string | number)[];
  /** Message */
  msg: string;
  /** Error Type */
  type: string;
  /** Input */
  input?: any;
  /** Context */
  ctx?: object;
}

export type QueryParamsType = Record<string | number, any>;
export type ResponseFormat = keyof Omit<Body, "body" | "bodyUsed">;

export interface FullRequestParams extends Omit<RequestInit, "body"> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseFormat;
  /** request body */
  body?: unknown;
  /** base url */
  baseUrl?: string;
  /** request cancellation token */
  cancelToken?: CancelToken;
}

export type RequestParams = Omit<
  FullRequestParams,
  "body" | "method" | "query" | "path"
>;

export interface ApiConfig<SecurityDataType = unknown> {
  baseUrl?: string;
  baseApiParams?: Omit<RequestParams, "baseUrl" | "cancelToken" | "signal">;
  securityWorker?: (
    securityData: SecurityDataType | null,
  ) => Promise<RequestParams | void> | RequestParams | void;
  customFetch?: typeof fetch;
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown>
  extends Response {
  data: D;
  error: E;
}

type CancelToken = Symbol | string | number;

export enum ContentType {
  Json = "application/json",
  JsonApi = "application/vnd.api+json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
  Text = "text/plain",
}

export class HttpClient<SecurityDataType = unknown> {
  public baseUrl: string = "";
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private abortControllers = new Map<CancelToken, AbortController>();
  private customFetch = (...fetchParams: Parameters<typeof fetch>) =>
    fetch(...fetchParams);

  private baseApiParams: RequestParams = {
    credentials: "same-origin",
    headers: {},
    redirect: "follow",
    referrerPolicy: "no-referrer",
  };

  constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
    Object.assign(this, apiConfig);
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected encodeQueryParam(key: string, value: any) {
    const encodedKey = encodeURIComponent(key);
    return `${encodedKey}=${encodeURIComponent(typeof value === "number" ? value : `${value}`)}`;
  }

  protected addQueryParam(query: QueryParamsType, key: string) {
    return this.encodeQueryParam(key, query[key]);
  }

  protected addArrayQueryParam(query: QueryParamsType, key: string) {
    const value = query[key];
    return value.map((v: any) => this.encodeQueryParam(key, v)).join("&");
  }

  protected toQueryString(rawQuery?: QueryParamsType): string {
    const query = rawQuery || {};
    const keys = Object.keys(query).filter(
      (key) => "undefined" !== typeof query[key],
    );
    return keys
      .map((key) =>
        Array.isArray(query[key])
          ? this.addArrayQueryParam(query, key)
          : this.addQueryParam(query, key),
      )
      .join("&");
  }

  protected addQueryParams(rawQuery?: QueryParamsType): string {
    const queryString = this.toQueryString(rawQuery);
    return queryString ? `?${queryString}` : "";
  }

  private contentFormatters: Record<ContentType, (input: any) => any> = {
    [ContentType.Json]: (input: any) =>
      input !== null && (typeof input === "object" || typeof input === "string")
        ? JSON.stringify(input)
        : input,
    [ContentType.JsonApi]: (input: any) =>
      input !== null && (typeof input === "object" || typeof input === "string")
        ? JSON.stringify(input)
        : input,
    [ContentType.Text]: (input: any) =>
      input !== null && typeof input !== "string"
        ? JSON.stringify(input)
        : input,
    [ContentType.FormData]: (input: any) => {
      if (input instanceof FormData) {
        return input;
      }

      return Object.keys(input || {}).reduce((formData, key) => {
        const property = input[key];
        formData.append(
          key,
          property instanceof Blob
            ? property
            : typeof property === "object" && property !== null
              ? JSON.stringify(property)
              : `${property}`,
        );
        return formData;
      }, new FormData());
    },
    [ContentType.UrlEncoded]: (input: any) => this.toQueryString(input),
  };

  protected mergeRequestParams(
    params1: RequestParams,
    params2?: RequestParams,
  ): RequestParams {
    return {
      ...this.baseApiParams,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...(this.baseApiParams.headers || {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected createAbortSignal = (
    cancelToken: CancelToken,
  ): AbortSignal | undefined => {
    if (this.abortControllers.has(cancelToken)) {
      const abortController = this.abortControllers.get(cancelToken);
      if (abortController) {
        return abortController.signal;
      }
      return void 0;
    }

    const abortController = new AbortController();
    this.abortControllers.set(cancelToken, abortController);
    return abortController.signal;
  };

  public abortRequest = (cancelToken: CancelToken) => {
    const abortController = this.abortControllers.get(cancelToken);

    if (abortController) {
      abortController.abort();
      this.abortControllers.delete(cancelToken);
    }
  };

  public request = async <T = any, E = any>({
    body,
    secure,
    path,
    type,
    query,
    format,
    baseUrl,
    cancelToken,
    ...params
  }: FullRequestParams): Promise<HttpResponse<T, E>> => {
    const secureParams =
      ((typeof secure === "boolean" ? secure : this.baseApiParams.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const queryString = query && this.toQueryString(query);
    const payloadFormatter = this.contentFormatters[type || ContentType.Json];
    const responseFormat = format || requestParams.format;

    return this.customFetch(
      `${baseUrl || this.baseUrl || ""}${path}${queryString ? `?${queryString}` : ""}`,
      {
        ...requestParams,
        headers: {
          ...(requestParams.headers || {}),
          ...(type && type !== ContentType.FormData
            ? { "Content-Type": type }
            : {}),
        },
        signal:
          (cancelToken
            ? this.createAbortSignal(cancelToken)
            : requestParams.signal) || null,
        body:
          typeof body === "undefined" || body === null
            ? null
            : payloadFormatter(body),
      },
    ).then(async (response) => {
      const r = response as HttpResponse<T, E>;
      r.data = null as unknown as T;
      r.error = null as unknown as E;

      const responseToParse = responseFormat ? response.clone() : response;
      const data = !responseFormat
        ? r
        : await responseToParse[responseFormat]()
            .then((data) => {
              if (r.ok) {
                r.data = data;
              } else {
                r.error = data;
              }
              return r;
            })
            .catch((e) => {
              r.error = e;
              return r;
            });

      if (cancelToken) {
        this.abortControllers.delete(cancelToken);
      }

      if (!response.ok) throw data;
      return data;
    });
  };
}

/**
 * @title FastShip
 * @version 0.1.0
 * @termsOfService https://fastship.vercel.app/terms
 * @contact FastShip Support <support@fastship.com> (https://fastship.vercel.app/support)
 *
 *
 * Delivery Management System for sellers and delivery agents
 *
 * ### Seller
 * - Submit shipments effortlessly
 * - Share tracking links with customers
 * - Receive notifications on shipment updates
 *
 * ### Delivery Agent
 * - Auto accept shipments
 * - Track and update shipment status
 * - Email and SMS notifications
 */
export class Api<
  SecurityDataType extends unknown,
> extends HttpClient<SecurityDataType> {
  /**
   * No description
   *
   * @name GetRoot
   * @summary Get Root
   * @request GET:/
   */
  getRoot = (params: RequestParams = {}) =>
    this.request<any, any>({
      path: `/`,
      method: "GET",
      format: "json",
      ...params,
    });

  shipment = {
    /**
     * No description
     *
     * @tags Shipment
     * @name GetShipment
     * @summary Get Shipment
     * @request GET:/shipment
     * @secure
     */
    getShipment: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipment`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Submit and Create a new **shipment**
     *
     * @tags Shipment
     * @name CreateShipment
     * @summary Create Shipment
     * @request POST:/shipment
     * @secure
     */
    createShipment: (data: ShipmentCreate, params: RequestParams = {}) =>
      this.request<ShipmentRead, void | HTTPValidationError>({
        path: `/shipment`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Shipment
     * @name GetReviewPage
     * @summary Get Review Page
     * @request GET:/shipment/review
     */
    getReviewPage: (
      query: {
        /** Token */
        token: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/shipment/review`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Shipment
     * @name SubmitReview
     * @summary Submit Review
     * @request POST:/shipment/review
     */
    submitReview: (
      query: {
        /** Token */
        token: string;
      },
      data: BodySubmitReview,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/shipment/review`,
        method: "POST",
        query: query,
        body: data,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Shipment
     * @name GetTaggedShipments
     * @summary Get Tagged Shipments
     * @request GET:/shipment/tagged
     */
    getTaggedShipments: (
      query: {
        tag_name: TagName;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead[], HTTPValidationError>({
        path: `/shipment/tagged`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Shipment
     * @name GetShipmentById
     * @summary Get Shipment By Id
     * @request GET:/shipment/{shipment_id}
     * @secure
     */
    getShipmentById: (shipmentId: string, params: RequestParams = {}) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipment/${shipmentId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Shipment
     * @name UpdateShipment
     * @summary Update Shipment
     * @request PUT:/shipment/{shipment_id}
     * @secure
     */
    updateShipment: (
      shipmentId: string,
      data: ShipmentUpdate,
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipment/${shipmentId}`,
        method: "PUT",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Shipment
     * @name PatchShipment
     * @summary Patch Shipment
     * @request PATCH:/shipment/{shipment_id}
     * @secure
     */
    patchShipment: (
      shipmentId: string,
      data: ShipmentPatch,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/shipment/${shipmentId}`,
        method: "PATCH",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Shipment
     * @name DeleteShipment
     * @summary Delete Shipment
     * @request DELETE:/shipment/{shipment_id}
     * @secure
     */
    deleteShipment: (shipmentId: string, params: RequestParams = {}) =>
      this.request<Record<string, any>, HTTPValidationError>({
        path: `/shipment/${shipmentId}`,
        method: "DELETE",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Shipment
     * @name CancelShipment
     * @summary Cancel Shipment
     * @request GET:/shipment/{shipment_id}/cancel
     * @secure
     */
    cancelShipment: (shipmentId: string, params: RequestParams = {}) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipment/${shipmentId}/cancel`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Shipment
     * @name AddTagToShipment
     * @summary Add Tag To Shipment
     * @request GET:/shipment/{shipment_id}/tag
     */
    addTagToShipment: (
      shipmentId: string,
      query: {
        tag_name: TagName;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipment/${shipmentId}/tag`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Shipment
     * @name RemoveTagFromShipment
     * @summary Remove Tag From Shipment
     * @request DELETE:/shipment/{shipment_id}/tag
     */
    removeTagFromShipment: (
      shipmentId: string,
      query: {
        tag_name: TagName;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipment/${shipmentId}/tag`,
        method: "DELETE",
        query: query,
        format: "json",
        ...params,
      }),
  };
  sellers = {
    /**
     * No description
     *
     * @tags Seller
     * @name RegisterSeller
     * @summary Register Seller
     * @request POST:/sellers
     */
    registerSeller: (data: CreateSeller, params: RequestParams = {}) =>
      this.request<ReadSeller, HTTPValidationError>({
        path: `/sellers`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name LoginSeller
     * @summary Login Seller
     * @request POST:/sellers/token
     */
    loginSeller: (data: BodyLoginSeller, params: RequestParams = {}) =>
      this.request<TokenData, HTTPValidationError>({
        path: `/sellers/token`,
        method: "POST",
        body: data,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name LogoutSeller
     * @summary Logout Seller
     * @request GET:/sellers/logout
     * @secure
     */
    logoutSeller: (params: RequestParams = {}) =>
      this.request<void, any>({
        path: `/sellers/logout`,
        method: "GET",
        secure: true,
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name GetSellerProfile
     * @summary Get Seller Profile
     * @request GET:/sellers/me
     * @secure
     */
    getSellerProfile: (params: RequestParams = {}) =>
      this.request<ReadSeller, any>({
        path: `/sellers/me`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name GetShipments
     * @summary Get Shipments
     * @request GET:/sellers/shipments
     * @secure
     */
    getShipments: (params: RequestParams = {}) =>
      this.request<ShipmentRead[], any>({
        path: `/sellers/shipments`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name VerifySellerEmail
     * @summary Verify Seller Email
     * @request GET:/sellers/verify
     */
    verifySellerEmail: (
      query: {
        /** Token */
        token: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/sellers/verify`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name ForgotPassword
     * @summary Forgot Password
     * @request GET:/sellers/forgot_password
     */
    forgotPassword: (
      query: {
        /**
         * Email
         * @format email
         */
        email: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/sellers/forgot_password`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name ResetPassword
     * @summary Reset Password
     * @request POST:/sellers/reset_password
     */
    resetPassword: (
      query: {
        /** Token */
        token: string;
      },
      data: BodyResetPassword,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/sellers/reset_password`,
        method: "POST",
        query: query,
        body: data,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name ResetPasswordForm
     * @summary Reset Password Form
     * @request GET:/sellers/reset_password_form
     */
    resetPasswordForm: (
      query: {
        /** Token */
        token: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/sellers/reset_password_form`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),
  };
  partners = {
    /**
     * No description
     *
     * @tags Delivery Partner
     * @name UpdateDeliveryPartner
     * @summary Update Delivery Partner
     * @request PUT:/partners
     * @secure
     */
    updateDeliveryPartner: (
      data: UpdateDeliveryPartner,
      params: RequestParams = {},
    ) =>
      this.request<ReadDeliveryPartner, HTTPValidationError>({
        path: `/partners`,
        method: "PUT",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name RegisterDeliveryPartner
     * @summary Register Delivery Partner
     * @request POST:/partners
     */
    registerDeliveryPartner: (
      data: CreateDeliveryPartner,
      params: RequestParams = {},
    ) =>
      this.request<ReadDeliveryPartner, HTTPValidationError>({
        path: `/partners`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name LoginDeliveryPartner
     * @summary Login Delivery Partner
     * @request POST:/partners/token
     */
    loginDeliveryPartner: (
      data: BodyLoginDeliveryPartner,
      params: RequestParams = {},
    ) =>
      this.request<TokenData, HTTPValidationError>({
        path: `/partners/token`,
        method: "POST",
        body: data,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name LogoutDeliveryPartner
     * @summary Logout Delivery Partner
     * @request GET:/partners/logout
     * @secure
     */
    logoutDeliveryPartner: (params: RequestParams = {}) =>
      this.request<void, any>({
        path: `/partners/logout`,
        method: "GET",
        secure: true,
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name GetDeliveryPartnerProfile
     * @summary Get Delivery Partner Profile
     * @request GET:/partners/me
     * @secure
     */
    getDeliveryPartnerProfile: (params: RequestParams = {}) =>
      this.request<ReadDeliveryPartner, any>({
        path: `/partners/me`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name GetShipments
     * @summary Get Shipments
     * @request GET:/partners/shipments
     * @secure
     */
    getShipments: (params: RequestParams = {}) =>
      this.request<ShipmentRead[], any>({
        path: `/partners/shipments`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name VerifySellerEmail
     * @summary Verify Seller Email
     * @request GET:/partners/verify
     */
    verifySellerEmail: (
      query: {
        /** Token */
        token: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/partners/verify`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name ForgotPassword
     * @summary Forgot Password
     * @request GET:/partners/forgot_password
     */
    forgotPassword: (
      query: {
        /**
         * Email
         * @format email
         */
        email: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/partners/forgot_password`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name ResetPassword
     * @summary Reset Password
     * @request POST:/partners/reset_password
     */
    resetPassword: (
      query: {
        /** Token */
        token: string;
      },
      data: BodyResetPassword,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/partners/reset_password`,
        method: "POST",
        query: query,
        body: data,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name ResetPasswordForm
     * @summary Reset Password Form
     * @request GET:/partners/reset_password_form
     */
    resetPasswordForm: (
      query: {
        /** Token */
        token: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/partners/reset_password_form`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),
  };
}
